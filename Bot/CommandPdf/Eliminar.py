import discord
from Clases import util
import os


async def eliminar(interation: discord.Interaction,NombreDeArchivo):
    """Pdf = [pdfs for pdfs in ListaArchivos if pdfs.startswith("Reporte " + NombreDeArchivo)]
    for pdf in Pdf:
        if pdf == f"Reporte {NombreDeArchivo}.pdf":
            os.remove(os.path.join(ruta_Pdfs, pdf))
            await ctx.send(embed=util.CrearMensajeEmbed("", "Archivo Eliminado Correctamente"))
            return
    await ctx.send(f"No se encontró el Id de archivo {NombreDeArchivo}")"""
    ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Apunta a Bot/
    ruta_Pdfs = os.path.join(ruta_base, 'Reportes')
    if not os.path.exists(ruta_Pdfs + "/" + NombreDeArchivo):
        await interation.response.send_message("Error al eliminar el Pdf, o No existe el pdf")
        return
    else:
        os.remove(f"./Bot/Reportes/{NombreDeArchivo}")
        await interation.response.send_message(embed=util.CrearMensajeEmbed("", "Archivo Eliminado Correctamente"))
        return
