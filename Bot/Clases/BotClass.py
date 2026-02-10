import discord
from discord.ext import commands
from Declaraciones.views import viewsPersistentes

class MyBot(commands.Bot):
    _instancia = None

    def __new__(cls,command_prefix,intents):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar(command_prefix,intents)
        return cls._instancia

    def _inicializar(self,command_prefix,intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self):
        await self.load_extension("cogs.Offices")
        await self.load_extension("cogs.Eventos")
        await self.load_extension("cogs.Moderacion")
        await self.tree.sync()
        VPS = await viewsPersistentes()
        self.add_view(VPS.vistaRegistro)

