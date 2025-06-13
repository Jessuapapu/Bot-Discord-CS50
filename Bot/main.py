import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Modulos propios
from Clases import util

# Cargamos el .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Permisos de Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

# Definimos el bot extendiendo Bot para usar setup_hook
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="$", intents=intents)

    async def setup_hook(self):
        await self.load_extension("cogs.Offices")  # Aquí cargas tu cog de Offices
        await self.tree.sync()
        print(" Slash commands sincronizados")

bot = MyBot()

@bot.command()
async def Obtenerpdf(ctx, Argumento, NombreDeArchivo = " "):
    ruta_Pdfs = "./Reportes"
    ListaArchivos = os.listdir(ruta_Pdfs)
    
    if Argumento.lower() not in util.ArgumentosBuscar + util.ArgumentosEliminar + util.ArgumentosListar:
        await ctx.send("Error en el Argumento de Inicialización.")
        return
    
    async def Listar():
        mensajeEmbebido = ""
        try:
            Pdf = [pdfs for pdfs in ListaArchivos]
            for pdf in Pdf:
                mensajeEmbebido += f"{pdf}\n"
            await ctx.send(embed=util.CrearMensajeEmbed("Lista de Archivos", mensajeEmbebido))
        except:
            await ctx.send("Error al cargar los pdfs")

    async def buscar():
        mensajeEmbebido = ""
        try:
            Pdf = [pdfs for pdfs in ListaArchivos if pdfs.startswith("Reporte " + NombreDeArchivo)]
            if not Pdf:
                await ctx.send(f"No se encontró el archivo {NombreDeArchivo}")
                return
            for pdf in Pdf:
                mensajeEmbebido += f"{pdf}\n"
            await ctx.send(embed=util.CrearMensajeEmbed("Archivos encontrados", mensajeEmbebido, discord.Color.green()))
        except:
            await ctx.send("Error al buscar el pdf")

    async def obtener():
        Pdf = [pdfs for pdfs in ListaArchivos if pdfs.startswith("Reporte " + NombreDeArchivo)]
        for pdf in Pdf:
            if pdf == f"Reporte {NombreDeArchivo}.pdf":
                await ctx.send(file=discord.File(os.path.join(ruta_Pdfs, pdf)))
                return
        await ctx.send(f"No se encontró el Id de archivo {NombreDeArchivo}")

    async def eliminar():
        Pdf = [pdfs for pdfs in ListaArchivos if pdfs.startswith("Reporte " + NombreDeArchivo)]
        for pdf in Pdf:
            if pdf == f"Reporte {NombreDeArchivo}.pdf":
                os.remove(os.path.join(ruta_Pdfs, pdf))
                await ctx.send(embed=util.CrearMensajeEmbed("", "Archivo Eliminado Correctamente"))
                return
        await ctx.send(f"No se encontró el Id de archivo {NombreDeArchivo}")

    if Argumento.lower() in util.ArgumentosBuscar:
        await buscar()
    elif Argumento.lower() in util.ArgumentosListar:
        await Listar()
    elif Argumento.lower() in util.ArgumentosObtener:
        await obtener()
    elif Argumento.lower() in util.ArgumentosEliminar:
        await eliminar()
    else:
        await ctx.send("Error al obtener el Argumento")
        return

# Finalmente arrancamos el bot
bot.run(TOKEN)
