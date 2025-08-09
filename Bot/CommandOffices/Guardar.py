
import discord
from Declaraciones import EstadoGlobal
import os
import datetime
import requests

Estado = EstadoGlobal.EstadoGlobal()

# Librerias para generar los PDFs -------------------------
#   Jinja La que genera el html a partir de una plantilla
from jinja2 import Environment, FileSystemLoader
#   xhtml2pdf genera el Pdf apartir del html generado con jinja (nota: NO sosporta bien el css y quedo mas o menos simple xd)
from xhtml2pdf import pisa

from Clases import util

async def guardar(interaction: discord.Interaction, ID):

    Contents = Estado.getOffices(ID)

    if Contents is None:
        await interaction.response.send_message("No se encontró la office con ese ID.")
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

    nombresStaff = []
    for staff in Contents.NombresStaff:
        nombresStaff.append(staff)

    ahora = datetime.datetime.now()
    html_renderizado = template.render({
        "Estudiantes": Contents.Usuarios,
        "Fecha": f"Día {ahora.day} del Mes {ahora.month}",
        "Bloque": Contents.bloque,
        "Offices": ID,
        "logo": os.path.join(ruta_plantillas, "Logo.png").replace("\\", "/"),
        "Staff": nombresStaff
    })

    ruta_pdf = os.path.join("./Reportes", f"Reporte {ID}.pdf")
    with open(ruta_pdf, "w+b") as resultado:
        pisa_status = pisa.CreatePDF(html_renderizado, dest=resultado)

    if pisa_status is None:
        await interaction.response.send_message("Error al generar el PDF.")
        return

    headerTabla = ["Nombre", "Grupo", "Tiempo", "votos"]
    contenidoTabla = []
    
    for Estu in Contents.Usuarios:
        contenidoTabla.append([Estu.IdUsuario, Estu.grupo, Estu.cumplimientoReal, Estado.OfficesRevision[ID].ListaDeVotos[Estu.IdUsuario]])  
    
    tabla = util.CrearTabla(headerTabla,contenidoTabla,None)
    embed = util.CrearMensajeEmbed("Lista de Estudiantes", f"```\n{tabla}\n```", discord.Color.dark_gold())

    lista_subida = [{"nombre": estu.Usuario.nick if estu.Usuario is not None else "No user (verificar bug)", "grupo": estu.grupo, "cumplimiento": estu.cumplimientoReal} for estu in Contents.Usuarios]

    if util.subir_office_sistema (
        estudiantes=lista_subida,
        fecha=datetime.datetime.now().strftime("%Y-%m-%d"),
        semana=Contents.bloque.split("-")[0].strip(),
        turno=Contents.bloque.split("-")[1].strip(),
        token=os.getenv("SYSTEM_API_KEY", "")
    ):
        await interaction.response.send_message("Offices guardada\nSe ha subido la asistencia al sistema correctamente", embed=embed, file=discord.File(ruta_pdf))
    else:
        await interaction.response.send_message("Offices guardada, SE HAN DETECTADO ERRORES\nERROR: No se ha podido subir la asistencia al sistema", embed=embed, file=discord.File(ruta_pdf))

    del Estado.OfficesRevision[ID]
    return