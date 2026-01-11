# main.py
import discord
from discord.ext import commands
import os

from dotenv import load_dotenv
from Declaraciones.views import viewsPersistentes

# singleton.py
from Declaraciones.EstadoGlobal import EstadoGlobal

# Instancia única de EstadoGlobal que se comparte en todo el proyecto
EG = EstadoGlobal()

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN", "")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="$", intents=intents)

    async def setup_hook(self):
        await self.load_extension("cogs.Offices")
        await self.load_extension("cogs.Eventos")
        await self.load_extension("cogs.Moderacion")
        await self.tree.sync()
        VPS = await viewsPersistentes()
        self.add_view(VPS.vistaRegistro)

bot = MyBot()

def run_bot():
    bot.run(TOKEN)

if __name__ == "__main__":
    run_bot()
