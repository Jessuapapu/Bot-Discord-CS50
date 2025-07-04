import discord
import os


async def obtener(interation : discord.Interaction, NombreDeArchivo):
    """Pdf = [pdfs for pdfs in ListaArchivos if pdfs.startswith("Reporte " + NombreDeArchivo)]
    for pdf in Pdf:
        if pdf == f"Reporte {NombreDeArchivo}.pdf":
            await ctx.send(file=discord.File(os.path.join(ruta_Pdfs, pdf)))
            return
    await ctx.send(f"No se encontró el Id de archivo {NombreDeArchivo}")"""
    
    if not os.path.exists(f"./Reportes/{NombreDeArchivo}"): 
        await interation.response.send_message("Error al cargar el pdf o no existe")
        return
    else:
        await interation.response.send_message(file=discord.File(f"./Reportes/{NombreDeArchivo}"))
        return