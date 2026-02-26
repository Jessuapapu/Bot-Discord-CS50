
import os, discord, asyncio
from dotenv import load_dotenv

from Clases.BotClass import MyBot

from Bot.Services import ServiceClass
from Clases import logs

# cargar logs
log = logs.Logs()

# cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN", None)
TOKEN_SERVER = os.getenv("LINK_SERVER", None)
API_KEY = os.getenv("API_SERVER",None)
DISCORD_ID_SERVER = os.getenv("DISCORD_ID_SERVER",None)

# cargar datos desde el servidor
async def load_services():
    SW = await ServiceClass.Services(TOKEN_SERVER,API_KEY)
    return SW

def main():
    if not TOKEN or not TOKEN_SERVER or not API_KEY or not DISCORD_ID_SERVER:
        print("Falta algun token de auntetificacion")
        return
    
    # declaracion de intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.voice_states = True
    bot = MyBot(command_prefix='$', intents=intents)

    # cargar services
    SW = asyncio.run(load_services())

    bot.run(TOKEN, reconnect=True)




if __name__ == "__main__":
    main()