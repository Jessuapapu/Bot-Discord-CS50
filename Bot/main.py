import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
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

try:
    base_path = sys._MEIPASS
except AttributeError:
    base_path = os.path.abspath(".")

bot_path = os.path.join(base_path, "Bot")
repo_path = os.path.abspath(os.path.join(bot_path, ".."))  # carpeta raíz con .git

if bot_path not in sys.path:
    sys.path.insert(0, bot_path)

if not os.path.exists(bot_path):
    print(f"ERROR: No se encontró la carpeta Bot en: {bot_path}")
    sys.exit(1)

if getattr(sys, "frozen", False):
    env_path = os.path.join(base_path, "Bot", ".env")
else:
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Bot", ".env")

load_dotenv(env_path)

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

    def get_repo_path(self):
        """
        Devuelve la ruta absoluta a la carpeta raíz del repo (donde está .git),
        que está un nivel arriba de la carpeta Bot.
        En modo PyInstaller busca la ruta del ejecutable y sube.
        """
        if getattr(sys, "frozen", False):
            exe_dir = os.path.dirname(sys.executable)
            repo_dir = os.path.abspath(os.path.join(exe_dir, ".."))
        else:
            current_file_dir = os.path.dirname(os.path.abspath(__file__))
            repo_dir = os.path.abspath(os.path.join(current_file_dir, "..", ".."))

        if not os.path.isdir(os.path.join(repo_dir, ".git")):
            print(f"Advertencia: No se encontró carpeta .git en {repo_dir}")
        return repo_dir

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
        repo = self.get_repo_path()
        self.logger.info(f"Chequeando actualizaciones en repo: {repo}")
        try:
            output = subprocess.check_output(
                ["git", "pull"],
                stderr=subprocess.STDOUT,
                cwd=repo
            )
            result = output.decode("utf-8")
            if "Already up to date" not in result:
                self.logger.info("Actualización detectada, reiniciando bot...")
                self.stop_bot()
                self.start_bot()
            else:
                self.logger.info("No hay actualizaciones nuevas.")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error al verificar actualizaciones: {e.output.decode('utf-8')}")

    def get_current_commit(self):
        repo = self.get_repo_path()
        try:
            output = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=repo,
                stderr=subprocess.STDOUT
            )
            return output.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error obteniendo commit actual: {e.output.decode('utf-8')}")
            return "Desconocido"

    def get_current_branch(self):
        repo = self.get_repo_path()
        try:
            output = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=repo,
                stderr=subprocess.STDOUT
            )
            return output.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error obteniendo branch actual: {e.output.decode('utf-8')}")
            return "Desconocido"

    def list_branches(self):
        repo = self.get_repo_path()
        try:
            output = subprocess.check_output(
                ["git", "branch", "--list"],
                cwd=repo,
                stderr=subprocess.STDOUT
            )
            branches = output.decode("utf-8").splitlines()
            return [b.strip().replace("* ", "") for b in branches]
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error obteniendo lista de branches: {e.output.decode('utf-8')}")
            return []

    def checkout_branch(self, branch_name):
        repo = self.get_repo_path()
        try:
            output = subprocess.check_output(
                ["git", "checkout", branch_name],
                cwd=repo,
                stderr=subprocess.STDOUT
            )
            self.logger.info(f"Cambiado a la rama {branch_name}")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error cambiando a rama {branch_name}: {e.output.decode('utf-8')}")
            return False

    def checkout_commit(self, commit_sha):
        repo = self.get_repo_path()
        try:
            output = subprocess.check_output(
                ["git", "checkout", commit_sha],
                cwd=repo,
                stderr=subprocess.STDOUT
            )
            self.logger.info(f"Cambiado al commit {commit_sha}")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error cambiando a commit {commit_sha}: {e.output.decode('utf-8')}")
            return False

    def get_commit_details(self):
        repo = self.get_repo_path()
        try:
            output = subprocess.check_output(
                ["git", "show", "-s", "--format=%H%n%an%n%ad%n%s", "HEAD"],
                cwd=repo,
                stderr=subprocess.STDOUT,
                text=True
            )
            lines = output.strip().split('\n')
            if len(lines) >= 4:
                commit_hash, author, date, message = lines[0], lines[1], lines[2], lines[3]
                return f"Commit: {commit_hash}\nAutor: {author}\nFecha: {date}\nMensaje: {message}"
            else:
                return "Detalles del commit no disponibles."
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error obteniendo detalles del commit: {e.output.decode('utf-8')}")
            return "Error obteniendo detalles del commit."

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
        self.git_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.bot_frame, text="Control Bot")
        self.notebook.add(self.ui_frame, text="Offices")
        self.notebook.add(self.git_frame, text="Git Repo")

        # Log text
        self.text_log = tk.Text(self.bot_frame, state='disabled', height=12)
        self.text_log.pack(fill=tk.X, padx=5, pady=5)

        # Bot control buttons
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

        # Offices Treeview
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
            columns=("Nombre", "Grupo", "TiempoTotal", "Cumplimiento"),
            show="headings",
            height=10
        )
        self.students_tree.heading("Nombre", text="Nombre")
        self.students_tree.heading("Grupo", text="Grupo")
        self.students_tree.heading("TiempoTotal", text="Tiempo (s)")
        self.students_tree.heading("Cumplimiento", text="Cumplimiento")
        self.students_tree.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)

        scrollbar = ttk.Scrollbar(self.frame_details, orient=tk.VERTICAL, command=self.students_tree.yview)
        self.students_tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=2, sticky='ns')

        self.selected_office_id = None

        self.update_offices_list()
        self.after(1000, self.update_offices_list)

        # -- Pestaña Git --

        self.label_commit = tk.Label(self.git_frame, text="Commit: cargando...")
        self.label_commit.pack(anchor="w", padx=5, pady=5)

        self.label_branch = tk.Label(self.git_frame, text="Branch: cargando...")
        self.label_branch.pack(anchor="w", padx=5, pady=5)

        self.text_commit_details = tk.Text(self.git_frame, height=5, state='disabled')
        self.text_commit_details.pack(fill=tk.X, padx=5, pady=5)

        self.branches_var = tk.StringVar(value=[])
        self.listbox_branches = tk.Listbox(self.git_frame, listvariable=self.branches_var, height=10)
        self.listbox_branches.pack(fill=tk.X, padx=5, pady=5)

        self.btn_checkout_branch = tk.Button(self.git_frame, text="Cambiar a rama", command=self.checkout_selected_branch)
        self.btn_checkout_branch.pack(pady=5)

        # Campo y botón para checkout por commit
        frame_commit = tk.Frame(self.git_frame)
        frame_commit.pack(pady=10, fill=tk.X, padx=5)

        tk.Label(frame_commit, text="Checkout por commit SHA:").pack(anchor="w")
        self.entry_commit_sha = tk.Entry(frame_commit)
        self.entry_commit_sha.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,5))

        self.btn_checkout_commit = tk.Button(frame_commit, text="Cambiar a commit", command=self.checkout_commit_sha)
        self.btn_checkout_commit.pack(side=tk.LEFT)

        self.refresh_git_info()

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
        self.after(2000, self.refresh_git_info)

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
            self.students_tree.insert("", "end", values=(est.IdUsuario, est.grupo, est.TiempoTotal, est.cumplimientoReal))

    def refresh_git_info(self):
        commit = self.bot_controller.get_current_commit()
        branch = self.bot_controller.get_current_branch()
        branches = self.bot_controller.list_branches()
        details = self.bot_controller.get_commit_details()

        self.label_commit.config(text=f"Commit: {commit}")
        self.label_branch.config(text=f"Branch: {branch}")

        self.text_commit_details.configure(state='normal')
        self.text_commit_details.delete("1.0", tk.END)
        self.text_commit_details.insert(tk.END, details)
        self.text_commit_details.configure(state='disabled')

        self.branches_var.set(branches)
        self.after(60000, self.refresh_git_info)

    def checkout_selected_branch(self):
        selection = self.listbox_branches.curselection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una rama primero.")
            return
        branch_name = self.listbox_branches.get(selection[0])
        success = self.bot_controller.checkout_branch(branch_name)
        if success:
            messagebox.showinfo("Éxito", f"Cambiado a la rama {branch_name}")
            self.refresh_git_info()
        else:
            messagebox.showerror("Error", f"No se pudo cambiar a la rama {branch_name}")

    def checkout_commit_sha(self):
        sha = self.entry_commit_sha.get().strip()
        if not sha:
            messagebox.showwarning("Advertencia", "Ingrese un SHA válido.")
            return
        success = self.bot_controller.checkout_commit(sha)
        if success:
            messagebox.showinfo("Éxito", f"Cambiado al commit {sha}")
            self.refresh_git_info()
        else:
            messagebox.showerror("Error", f"No se pudo cambiar al commit {sha}")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("ERROR: No se encontró la variable de entorno TOKEN.")
        sys.exit(1)

    app = App(token)
    app.mainloop()
