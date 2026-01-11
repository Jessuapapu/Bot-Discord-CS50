import discord
import os


async def obtener(interation : discord.Interaction, NombreDeArchivo):
    if not os.path.exists(f"./Reportes/{NombreDeArchivo}"): 
        await interation.response.send_message("Error al cargar el pdf o no existe")
        return
    else:
        await interation.response.send_message(file=discord.File(f"./Reportes/{NombreDeArchivo}"))
        return