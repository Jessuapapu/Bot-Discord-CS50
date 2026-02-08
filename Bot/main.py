# main.py
import discord
from discord.ext import commands
import os

from dotenv import load_dotenv
from Declaraciones.views import viewsPersistentes
import requests
# singleton.py

from Services import ServiceOffices

from Clases import logs

# Instancia única de EstadoGlobal que se comparte en todo el proyecto
log = logs.Logs()

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN", None)
TOKEN_SERVER = os.getenv("LINK_SERVER", None)
API_KEY = os.getenv("API_SERVER",None)




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
    bot.run(TOKEN, reconnect=True)

def main():
    if not TOKEN or not TOKEN_SERVER or not API_KEY:
        print("Falta algun token de auntetificacion")
        return
    

    SW = ServiceOffices.Services(TOKEN_SERVER,API_KEY)

    SW.getCacheOffices()
    run_bot()

    
    

if __name__ == "__main__":
    main()