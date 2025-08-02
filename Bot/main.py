import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage
import logging
import asyncio
from dotenv import load_dotenv
import subprocess
import importlib

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Obtener base_path según si está en exe o no
try:
    base_path = sys._MEIPASS
except AttributeError:
    base_path = os.path.abspath(".")

bot_path = os.path.join(base_path, "Bot")

# Agregar bot_path a sys.path para importar módulos desde Bot/
if bot_path not in sys.path:
    sys.path.insert(0, bot_path)

# Verificar existencia de carpeta Bot para evitar errores
if not os.path.exists(bot_path):
    print(f"ERROR: No se encontró la carpeta Bot en: {bot_path}")
    sys.exit(1)

# Cargar variables de entorno (.env) desde Bot/.env dentro del exe o en desarrollo
if getattr(sys, "frozen", False):
    env_path = os.path.join(base_path, "Bot", ".env")
else:
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Bot", ".env")


load_dotenv(env_path)

# Cargar dinámicamente módulos dentro de carpetas Command* en Bot/
command_dirs = [d for d in os.listdir(bot_path) if d.startswith("Command") and os.path.isdir(os.path.join(bot_path, d))]

for cmd_dir in command_dirs:
    cmd_path = os.path.join(bot_path, cmd_dir)
    for file in os.listdir(cmd_path):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = f"{cmd_dir}.{file[:-3]}"
            try:
                importlib.import_module(module_name)
                print(f"Cargado módulo {module_name}")
            except Exception as e:
                print(f"Error cargando {module_name}: {e}")

# Importar librerías después para evitar conflictos con pyinstaller y sys.path
import discord
from discord.ext import commands
from Declaraciones.Declaraciones import EstadoGlobal

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.voice_states = True
        super().__init__(command_prefix="$", intents=intents)

    async def setup_hook(self):
        try:
            await self.load_extension("cogs.Offices")
            await self.load_extension("cogs.Eventos")
            await self.tree.sync()
        except Exception as e:
            print(f"Error cargando cogs: {e}")

class BotController:
    def __init__(self, token, log_widget):
        self.token = token
        self.bot = None
        self.log_widget = log_widget
        self.loop = None
        self.thread = None
        self.is_starting = False
        self.is_running = False

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger()
        self.logger.addHandler(self.TextHandler(self.log_widget))

    class TextHandler(logging.Handler):
        def __init__(self, text_widget):
            super().__init__()
            self.text_widget = text_widget

        def emit(self, record):
            msg = self.format(record)

            def append():
                self.text_widget.configure(state='normal')
                self.text_widget.insert(tk.END, msg + '\n')
                self.text_widget.configure(state='disabled')
                self.text_widget.yview(tk.END)

            self.text_widget.after(0, append)

    def start_bot(self):
        if self.is_starting or self.is_running:
            self.logger.info("Bot ya está corriendo o iniciando.")
            return

        def run_bot():
            self.is_starting = True
            self.bot = MyBot()
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            try:
                self.loop.run_until_complete(self.bot.start(self.token))
            except Exception as e:
                self.logger.error(f"Error en bot: {e}")
            finally:
                try:
                    self.loop.run_until_complete(self.bot.close())
                except Exception as e:
                    self.logger.error(f"Error al cerrar bot: {e}")
                self.loop.close()
                self.is_running = False
                self.is_starting = False

        self.thread = threading.Thread(target=run_bot, daemon=True)
        self.thread.start()
        self.is_running = True
        self.logger.info("Bot iniciado.")

    def stop_bot(self):
        if not self.is_running and not self.is_starting:
            self.logger.info("Bot ya está detenido.")
            return

        self.logger.info("Deteniendo bot...")
        try:
            if self.bot and self.loop:
                future = asyncio.run_coroutine_threadsafe(self.bot.close(), self.loop)
                future.result(timeout=10)
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=10)
        except Exception as e:
            self.logger.error(f"Error al detener bot: {e}")
        finally:
            self.is_running = False
            self.is_starting = False
            self.logger.info("Bot detenido.")

    def check_for_updates(self):
        try:
            output = subprocess.check_output(["git", "pull"], stderr=subprocess.STDOUT)
            result = output.decode("utf-8")
            if "Already up to date" not in result:
                self.logger.info("Actualización detectada, reiniciando bot...")
                self.stop_bot()
                self.start_bot()
            else:
                self.logger.info("No hay actualizaciones nuevas.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error al verificar actualizaciones: {e.output.decode('utf-8')}")

class App(tk.Tk):
    def __init__(self, token):
        super().__init__()
        self.title("Bot Discord Admin")
        self.geometry("960x720")

        ruta_icono = resource_path("Bot/Plantilla/Logo.png")
        self.icon_img = PhotoImage(file=ruta_icono)
        self.iconphoto(False, self.icon_img)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.bot_frame = ttk.Frame(self.notebook)
        self.ui_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.bot_frame, text="Control Bot")
        self.notebook.add(self.ui_frame, text="Offices")

        self.text_log = tk.Text(self.bot_frame, state='disabled', height=12)
        self.text_log.pack(fill=tk.X, padx=5, pady=5)

        frame_bot = tk.Frame(self.bot_frame)
        frame_bot.pack(pady=5)

        self.btn_start = tk.Button(frame_bot, text="Iniciar Bot", command=self.start_bot)
        self.btn_start.pack(side=tk.LEFT, padx=5)

        self.btn_stop = tk.Button(frame_bot, text="Detener Bot", command=self.stop_bot)
        self.btn_stop.pack(side=tk.LEFT, padx=5)
        
        self.btn_update = tk.Button(frame_bot, text="Actualizar Repo", command=self.update_repo)
        self.btn_update.pack(side=tk.LEFT, padx=5)

        self.bot_controller = BotController(token, self.text_log)

        self.update_buttons_state()
        self.after(1000, self.check_updates_loop)

        self.tree = ttk.Treeview(self.ui_frame, columns=("Id", "Creador"), show="headings", height=10)
        self.tree.heading("Id", text="ID Office")
        self.tree.heading("Creador", text="Creador")
        self.tree.pack(fill=tk.X, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_office_select)

        self.frame_details = tk.Frame(self.ui_frame)
        self.frame_details.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.label_office_id = tk.Label(self.frame_details, text="ID Office: ")
        self.label_office_id.grid(row=0, column=0, sticky="w")
        self.label_creador = tk.Label(self.frame_details, text="Creada por: ")
        self.label_creador.grid(row=1, column=0, sticky="w")
        self.label_staff = tk.Label(self.frame_details, text="Staff: ")
        self.label_staff.grid(row=2, column=0, sticky="w")
        self.label_horacreacion = tk.Label(self.frame_details, text="Hora Creación: ")
        self.label_horacreacion.grid(row=3, column=0, sticky="w")
        self.label_bloque = tk.Label(self.frame_details, text="Bloque: ")
        self.label_bloque.grid(row=4, column=0, sticky="w")
        self.label_estado = tk.Label(self.frame_details, text="Estado: ")
        self.label_estado.grid(row=5, column=0, sticky="w")

        self.students_tree = ttk.Treeview(
            self.frame_details,
            columns=("Nombre", "Grupo", "Tiempo (S)", "Cumplimiento"),
            show="headings",
            height=10
        )
        self.students_tree.heading("Nombre", text="Nombre")
        self.students_tree.heading("Grupo", text="Grupo")
        self.students_tree.heading("Tiempo (s)", text="Tiempo (s)")
        self.students_tree.heading("Cumplimiento", text="Cumplimiento")
        self.students_tree.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)

        scrollbar = ttk.Scrollbar(self.frame_details, orient=tk.VERTICAL, command=self.students_tree.yview)
        self.students_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=2, sticky='ns')

        self.selected_office_id = None

        self.update_offices_list()
        self.after(1000, self.update_offices_list)

    def update_buttons_state(self):
        running = self.bot_controller.is_running or self.bot_controller.is_starting
        self.btn_start.config(state=tk.DISABLED if running else tk.NORMAL)
        self.btn_stop.config(state=tk.NORMAL if running else tk.DISABLED)
        self.btn_update.config(state=tk.NORMAL)

        self.after(1000, self.update_buttons_state)

    def start_bot(self):
        threading.Thread(target=self.bot_controller.start_bot, daemon=True).start()

    def stop_bot(self):
        threading.Thread(target=self.bot_controller.stop_bot, daemon=True).start()

    def update_repo(self):
        threading.Thread(target=self.bot_controller.check_for_updates, daemon=True).start()

    def check_updates_loop(self):
        self.bot_controller.check_for_updates()
        self.after(60000, self.check_updates_loop)

    def update_offices_list(self):
        estado = EstadoGlobal()
        offices = estado.getKeyOfficesLista()

        for i in self.tree.get_children():
            self.tree.delete(i)

        for office_id in offices:
            office = estado.getOffices(office_id)
            if office:
                usuarios_str = ", ".join([u.IdUsuario for u in office.Usuarios])
                self.tree.insert("", "end", values=(office_id, usuarios_str))

        if self.selected_office_id:
            self.update_office_details()

        self.after(1000, self.update_offices_list)

    def on_office_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        self.selected_office_id = self.tree.item(selected[0])["values"][0]
        self.update_office_details()

    def update_office_details(self):
        if not self.selected_office_id:
            return

        estado = EstadoGlobal()
        office = estado.getOffices(self.selected_office_id)
        if not office:
            return

        self.label_office_id.config(text=f"ID Office: {office.Id}")
        self.label_creador.config(text=f"Creada por: {office.IdUsuario}")
        self.label_staff.config(text=f"Staff: {', '.join(office.NombresStaff)}")
        self.label_horacreacion.config(text=f"Hora Creación: {office.HoraCreacion}")
        self.label_bloque.config(text=f"Bloque: {office.bloque}")
        self.label_estado.config(text=f"Estado: {'Activa' if office.Estado == 1 else 'Finalizada'}")

        current_items = self.students_tree.get_children()
        estudiantes_dict = {e.IdUsuario: e for e in office.Usuarios}

        for item_id in current_items:
            uid = self.students_tree.item(item_id)['values'][0]
            if uid in estudiantes_dict:
                est = estudiantes_dict[uid]
                current_values = self.students_tree.item(item_id)['values']
                new_values = (est.IdUsuario, est.grupo, est.TiempoTotal, est.cumplimientoReal)
                if current_values != new_values:
                    self.students_tree.item(item_id, values=new_values)
                del estudiantes_dict[uid]
            else:
                self.students_tree.delete(item_id)

        for uid, est in estudiantes_dict.items():
            self.students_tree.insert(
                "",
                "end",
                values=(est.IdUsuario, est.grupo, est.TiempoTotal, est.cumplimientoReal)
            )


if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        print("Falta definir la variable DISCORD_TOKEN en el entorno")
    else:
        app = App(TOKEN)
        app.mainloop()
