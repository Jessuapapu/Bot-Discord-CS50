import discord
from discord.ext import commands
from discord import app_commands

from Clases import util
from Clases.Decoradores import valida_id_office, valida_roles 
from CommandOffices import Empezar, Finalizar, Guardar, Votaciones, Ruleta, Editar
from CommandPdf import Obtener, Eliminar

class Offices(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    offices = app_commands.Group(name="offices", description="Comando para gestionar offices")


    @offices.command(name="empezar", description="Inicia una office")
    @app_commands.describe(id="ID de la Office", canalvoz="Nombre del canal de voz")
    @valida_roles()
    async def empezar(self, interaction: discord.Interaction, id: str, canalvoz: discord.VoiceChannel):
        await Empezar.empezar(interaction, id, canalvoz)



    @offices.command(name="terminar", description="Finaliza una office")
    @app_commands.describe(id="ID de la Office")
    @app_commands.autocomplete(id=util.officesActivasId_autocomplete)
    @valida_roles()
    @valida_id_office()
    async def terminar(self, interaction: discord.Interaction, id: str):
        await Finalizar.finalizar(interaction, id)



    @offices.command(name="guardar", description="Guarda una office")
    @app_commands.describe(id="ID de la Office")
    @app_commands.autocomplete(id=util.officesRevisionId_autocomplete)
    @valida_roles()
    @valida_id_office()
    async def guardar(self, interaction: discord.Interaction, id: str):
        await Guardar.guardar(interaction, id)
        
        
        
    @offices.command(name="pdf", description="comando para obtener los pdf de las offices")
    @app_commands.describe(argumento = "Accion a realizar", nombre = "Nombre del archivo")
    @app_commands.choices(argumento=[
        discord.app_commands.Choice(name='Obtener', value="Obtener"),
        discord.app_commands.Choice(name='Eliminar', value="Eliminar")
    ])
    @app_commands.autocomplete(nombre=util.Pdfs_autocomplete)
    @valida_roles()
    async def pdf(self,interation: discord.Interaction, argumento: discord.app_commands.Choice[str], nombre:str):
        match argumento.value:
            case "Obtener":
                await Obtener.obtener(interation,nombre)
                return
            case "Eliminar":
                await Eliminar.eliminar(interation,nombre)  
                return
        
        # Si no se retorna con ninguno de los casos
        await interation.response.send_message("Error en el accion a realizar")
        
        return  



    @offices.command(name="votacion", description="Realiza una votacion para los activos")
    @app_commands.describe(id="Id de offices activa",tiempo="el tiempo que esta activa la votacion")
    @app_commands.choices(tiempo=[
        discord.app_commands.Choice(name='5 minutos', value=300.0),
        discord.app_commands.Choice(name='10 minutos', value=600.0)
    ])
    @app_commands.autocomplete(id=util.officesActivasId_autocomplete)
    @valida_roles()
    @valida_id_office()
    async def votaciones(self,interation:discord.Interaction, id:str, tiempo: discord.app_commands.Choice[float]):
        await Votaciones.votacion(interation,id,tiempo.value)
        
    
    
    @offices.command(name="ruleta", description="Inicia una ruleta para la offices")
    @app_commands.describe(canalvoz="Nombre del canal de voz")
    @valida_roles()
    async def ruleta(self, interaction: discord.Interaction, canalvoz: discord.VoiceChannel):
        await Ruleta.ruletita(interaction,canalvoz)
        
    
    
    @offices.command(name="editar", description="Edita una office ya terminada")
    @app_commands.describe(id="ID de la Office")
    @app_commands.autocomplete(id=util.officesRevisionId_autocomplete)
    @valida_roles()
    @valida_id_office()
    async def editar(self, interaction: discord.Interaction, id: str):
        await Editar.Editar(interaction,id)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Offices(bot))
