import discord
from discord.ext import commands
from discord import app_commands

from Clases import util
from CommandOffices import Empezar, Finalizar, Guardar
from CommandPdf import Obtener, Eliminar

class Offices(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    offices = app_commands.Group(name="offices", description="Comando para gestionar offices")

    @offices.command(name="empezar", description="Inicia una office")
    @app_commands.describe(id="ID de la Office", canalvoz="Nombre del canal de voz")
    async def empezar(self, interaction: discord.Interaction, id: str, canalvoz: discord.VoiceChannel):
        await Empezar.empezar(interaction, id, canalvoz)

    @offices.command(name="terminar", description="Finaliza una office")
    @app_commands.describe(id="ID de la Office")
    @app_commands.autocomplete(id=util.officesId_autocomplete)
    async def terminar(self, interaction: discord.Interaction, id: str):
        await Finalizar.finalizar(interaction, id)

    @offices.command(name="guardar", description="Guarda una office")
    @app_commands.describe(id="ID de la Office")
    @app_commands.autocomplete(id=util.officesId_autocomplete)
    async def guardar(self, interaction: discord.Interaction, id: str):
        await Guardar.guardar(interaction, id)
        
    @offices.command(name="pdf", description="comando para obtener los pdf de las offices")
    @app_commands.describe(argumento = "Accion a realizar", nombre = "Nombre del archivo")
    @app_commands.choices(argumento=[
        discord.app_commands.Choice(name='Obtener', value="Obtener"),
        discord.app_commands.Choice(name='Eliminar', value="Eliminar")
    ])
    @app_commands.autocomplete(nombre=util.Pdfs_autocomplete)
    async def pdf(self,interation: discord.Interaction, argumento: discord.app_commands.Choice[str], nombre:str):
        match argumento.value:
            case "Obtener":
                await Obtener.obtener(interation,nombre)
            case "Eliminar":
                await Eliminar.eliminar(interation,nombre)  
        return  

async def setup(bot: commands.Bot):
    await bot.add_cog(Offices(bot))
