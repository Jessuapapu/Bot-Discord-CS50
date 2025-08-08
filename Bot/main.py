import discord
from discord.ext import commands
import os, asyncio
from dotenv import load_dotenv
import webserver
from Declaraciones.views import viewsPersistentes
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
        await self.load_extension("cogs.Offices")
        await self.load_extension("cogs.Eventos")
        await self.load_extension("cogs.Moderacion")
        await self.tree.sync()
        
        
        # vistasPersistentes
        VPS = await viewsPersistentes()
        
        self.add_view(VPS.vistaRegistro)


bot = MyBot()


# Finalmente arrancamos el bot
# webserver.keep_alive()
bot.run(TOKEN)
