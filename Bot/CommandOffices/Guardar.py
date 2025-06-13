
import discord
from Declaraciones import Declaraciones
import os
import datetime

from Clases import util
Estado = Declaraciones.EstadoGlobal()

# Librerias para generar los PDFs -------------------------
#   Jinja La que genera el html a partir de una plantilla
from jinja2 import Environment, FileSystemLoader
#   xhtml2pdf genera el Pdf apartir del html generado con jinja (nota: NO sosporta bien el css y quedo mas o menos simple xd)
from xhtml2pdf import pisa

from Clases import util


async def guardar(interaction: discord.Interaction, ID):
    try:
        Contents = Estado.OfficesLista[ID]
    except:
        await interaction.response.send_message("No se encontró la offices.")
        return

    if Contents.Estado != 0:
        await interaction.response.send_message("No se ha finalizado la offices.")
        return
    
    # Hace falta el formato de los estudiantes (Solucionado)
    """Estudiantes = [
        util.fomratoEstudiante(user.IdUsuario, user.TiempoTotal)
        for user in 
    ]
    """
    
    ruta_base = os.path.dirname(os.path.dirname(__file__))
    ruta_plantillas = os.path.join(ruta_base, 'Plantilla')
    # Configuramos Jinja
    env = Environment(loader=FileSystemLoader(ruta_plantillas))
    template = env.get_template('Plantilla.html')

    ahora = datetime.now()
    html_renderizado = template.render({
        "Estudiantes": Contents.Usuarios,
        "Fecha": f"Día {ahora.day} del Mes {ahora.month}",
        "Offices": ID,
        "logo": os.path.join(ruta_plantillas, "Logo.png").replace("\\", "/")
    })

    ruta_pdf = os.path.join("./Reportes", f"Reporte {ID}.pdf")
    with open(ruta_pdf, "w+b") as resultado:
        pisa_status = pisa.CreatePDF(html_renderizado, dest=resultado)

    if pisa_status.err:
        await interaction.response.send_message.send("Error al generar el PDF.")
        return

    mensajeEmbebido = ""
    for Estu in Contents.Usuarios:
        mensajeEmbebido += Estu.toString()

    del Estado.OfficesLista[ID]
    await interaction.response.send_message(embed=util.CrearMensajeEmbed("Guardando estos estudiantes", mensajeEmbebido), file=discord.File(ruta_pdf))
    return