# main.py
import discord
from discord.ext import commands
import os, asyncio
from dotenv import load_dotenv
import threading
from webserver import app
from Declaraciones.views import viewsPersistentes
from Declaraciones.EstadoGlobal import EstadoGlobal

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
    
    # Flask en el hilo principal → permite recarga automática
    app.run(host="0.0.0.0", port=10000, debug=True)
