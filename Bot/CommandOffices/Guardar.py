
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

    Contents = Estado.OfficesRevision[ID]

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

    ahora = datetime.datetime.now()
    html_renderizado = template.render({
        "Estudiantes": Contents.Usuarios,
        "Fecha": f"Día {ahora.day} del Mes {ahora.month}",
        "Bloque": Contents.bloque,
        "Offices": ID,
        "logo": os.path.join(ruta_plantillas, "Logo.png").replace("\\", "/")
    })

    ruta_pdf = os.path.join("./Reportes", f"Reporte {ID}.pdf")
    with open(ruta_pdf, "w+b") as resultado:
        pisa_status = pisa.CreatePDF(html_renderizado, dest=resultado)

    if pisa_status.err:
        await interaction.response.send_message.send("Error al generar el PDF.")
        return

    headerTabla = ["Nombre", "Grupo", "Cumplimiento", "votos"]
    contenidoTabla = []
    
    mensajeEmbebido = ""
    for Estu in Contents.Usuarios:
        contenidoTabla.append([Estu.IdUsuario, Estu.grupo, Estu.cumplimientoReal, Estado.OfficesRevision[ID].ListaDeVotos[Estu.IdUsuario]])  
    
    tabla = util.CrearTabla(headerTabla,contenidoTabla)
    embed = util.CrearMensajeEmbed("Lista de Estudiantes", f"```\n{tabla}\n```", discord.Color.dark_gold())

    del Estado.OfficesRevision[ID]
    await interaction.response.send_message(embed=embed, file=discord.File(ruta_pdf))
    return