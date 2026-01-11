import discord
from Clases import util
import os


async def eliminar(interation: discord.Interaction,NombreDeArchivo):
    if not os.path.exists(f"./Reportes/{NombreDeArchivo}"):
        await interation.response.send_message("Error al eliminar el Pdf, o No existe el pdf")
        return

    os.remove(f"./Reportes/{NombreDeArchivo}")
    await interation.response.send_message(embed=util.CrearMensajeEmbed("", "Archivo Eliminado Correctamente"))
    return
