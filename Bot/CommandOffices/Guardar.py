import discord
from Declaraciones import Declaraciones
import os
import datetime

Estado = Declaraciones.EstadoGlobal()

# Librerías para generar PDFs
from jinja2 import Environment, FileSystemLoader
from xhtml2pdf import pisa

from Clases import util

async def guardar(interaction: discord.Interaction, ID):

    Contents = Estado.getOffices(ID)

    if Contents.Estado != 0:
        await interaction.response.send_message("No se ha finalizado la offices.")
        return

    # Rutas relativas partiendo desde este archivo:
    ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Apunta a Bot/
    ruta_plantillas = os.path.join(ruta_base, 'Plantilla')
    ruta_reportes = os.path.join(ruta_base, 'Reportes')
    os.makedirs(ruta_reportes, exist_ok=True)  # Crea carpeta Reportes si no existe

    # Configurar Jinja
    env = Environment(loader=FileSystemLoader(ruta_plantillas))
    template = env.get_template('Plantilla.html')

    nombresStaff = [staff for staff in Contents.NombresStaff]

    ahora = datetime.datetime.now()
    html_renderizado = template.render({
        "Estudiantes": Contents.Usuarios,
        "Fecha": f"Día {ahora.day} del Mes {ahora.month}",
        "Bloque": Contents.bloque,
        "Offices": ID,
        "logo": os.path.join(ruta_plantillas, "Logo.png").replace("\\", "/"),
        "Staff": nombresStaff
    })

    ruta_pdf = os.path.join(ruta_reportes, f"Reporte {ID}.pdf")
    with open(ruta_pdf, "w+b") as resultado:
        pisa_status = pisa.CreatePDF(html_renderizado, dest=resultado)

    if pisa_status.err:
        await interaction.response.send_message("Error al generar el PDF.")
        return

    headerTabla = ["Nombre", "Grupo", "Tiempo", "votos"]
    contenidoTabla = []
    
    for Estu in Contents.Usuarios:
        contenidoTabla.append([
            Estu.IdUsuario,
            Estu.grupo,
            Estu.cumplimientoReal,
            Estado.OfficesRevision[ID].ListaDeVotos[Estu.IdUsuario]
        ])  
    
    tabla = util.CrearTabla(headerTabla, contenidoTabla, None)
    embed = util.CrearMensajeEmbed("Lista de Estudiantes", f"```\n{tabla}\n```", discord.Color.dark_gold())

    del Estado.OfficesRevision[ID]
    await interaction.response.send_message(embed=embed, file=discord.File(ruta_pdf))
