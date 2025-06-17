
import discord
from discord.ext import commands
from discord import app_commands


from Clases import util
from CommandOffices import Empezar, Finalizar, Guardar
from CommandPdf import Obtener, Eliminar


class Eventos(commands.Cog):
    
    def __init__(self,bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_mensaje(self,message):
        if message.author.bot:
            return
    
    

        