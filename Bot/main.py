# main.py
import discord
from discord.ext import commands
import sys, os

from dotenv import load_dotenv
import threading
from Declaraciones.views import viewsPersistentes

# singleton.py
from Declaraciones.EstadoGlobal import EstadoGlobal

# Instancia única de EstadoGlobal que se comparte en todo el proyecto
EG = EstadoGlobal()

# importar el serverweb
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from WebserverApp import webserver

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
    # Iniciamos el bot en segundo plano
    threading.Thread(target=run_bot, daemon=True).start()

    webserver.socketio.run(app=webserver.app,host="0.0.0.0", port=10000)
