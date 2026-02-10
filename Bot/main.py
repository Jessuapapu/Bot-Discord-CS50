
import os, discord
from dotenv import load_dotenv

from Clases.BotClass import MyBot

from Services import ServiceOffices
from Clases import logs

# Instancia única de EstadoGlobal que se comparte en todo el proyecto
log = logs.Logs()

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN", None)
TOKEN_SERVER = os.getenv("LINK_SERVER", None)
API_KEY = os.getenv("API_SERVER",None)


def main():
    if not TOKEN or not TOKEN_SERVER or not API_KEY:
        print("Falta algun token de auntetificacion")
        return
    
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    intents.voice_states = True
    bot = MyBot(command_prefix='$', intents=intents )

    SW = ServiceOffices.Services(TOKEN_SERVER,API_KEY)

    SW.getCacheOffices()
    bot.run(TOKEN, reconnect=True)

    

if __name__ == "__main__":
    main()