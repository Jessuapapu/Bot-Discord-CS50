import discord
import os


async def obtener(interation : discord.Interaction, NombreDeArchivo):
    """Pdf = [pdfs for pdfs in ListaArchivos if pdfs.startswith("Reporte " + NombreDeArchivo)]
    for pdf in Pdf:
        if pdf == f"Reporte {NombreDeArchivo}.pdf":
            await ctx.send(file=discord.File(os.path.join(ruta_Pdfs, pdf)))
            return
    await ctx.send(f"No se encontró el Id de archivo {NombreDeArchivo}")"""
    
    ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Apunta a Bot/
    ruta_Pdfs = os.path.join(ruta_base, 'Reportes')
    if not os.path.exists(ruta_Pdfs + "/" + NombreDeArchivo): 
        await interation.response.send_message("Error al cargar el pdf o no existe")
        return
    else:
        await interation.response.send_message(file=discord.File(ruta_Pdfs + "/" + NombreDeArchivo))
        return