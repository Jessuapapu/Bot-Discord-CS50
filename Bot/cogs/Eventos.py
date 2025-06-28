import discord
from discord.ext import commands
import re
import time

import asyncio
from Declaraciones import Declaraciones
from Clases import util, Botones
Estado = Declaraciones.EstadoGlobal()



# Diccionario para rastrear mensajes recientes por usuario
spam_tracker = {}

# Lista de dominios maliciosos
malicious_domains = [
    "grabify.link", "iplogger.org", "gyazo.nl", "discord.gift", "free-nitro.com", "discodapp.com", "steamcommunity.com"
]

# Regex para encontrar URLs
url_regex = r"(https?://[^\s]+)"

# Configuración de límites
SPAM_INTERVAL = 5        # Tiempo en segundos
SPAM_THRESHOLD = 10        # Cantidad de mensajes permitidos en el intervalo


class Eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ESTE CODIGO NO ES MIO SOLO LO AGARRE DE UNA PLANTILLA XD
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        user_id = message.author.id
        now = time.time()

        # --- Anti-Link Malicioso ---
        urls = re.findall(url_regex, message.content.lower())
        for url in urls:
            for domain in malicious_domains:
                if domain in url:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention}, ese link está bloqueado.")
                    return

        # --- Anti-Spam ---
        if user_id not in spam_tracker:
            spam_tracker[user_id] = []
        spam_tracker[user_id].append(now)

        # Filtrar mensajes fuera del intervalo
        spam_tracker[user_id] = [t for t in spam_tracker[user_id] if now - t < SPAM_INTERVAL]

        if len(spam_tracker[user_id]) > SPAM_THRESHOLD:
            await message.delete()
            return
        
        
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        user_id = str(member.display_name[10:])
        AutorRoles = [rol.name for rol in member.roles] 
        
        if any(rol in ["Staff", "Admin Staff"] for rol in AutorRoles):
            return
        
        # SALIDA DEL CANAL DE VOZ
        if before.channel and (after.channel is None or before.channel != after.channel):
            if before.channel.id in Estado.CanalesDeVoz and user_id in Estado.ContadoresActivos:
                estudiante, tarea = Estado.ContadoresActivos[user_id]
                await estudiante.DetenerContador(tarea)
                #Estado.ContadoresActivos[user_id] = (estudiante, tarea)

        # ENTRADA A CANAL DE VOZ
        elif after.channel and after.channel.id in Estado.CanalesDeVoz:
            if user_id in Estado.ContadoresActivos:
                # Ya está registrado, solo se reactiva el contador
                estudiante, _ = Estado.ContadoresActivos[user_id]
                nueva_tarea = asyncio.create_task(estudiante.CalcularTiempo())
                Estado.ContadoresActivos[user_id] = (estudiante, nueva_tarea)
            else:
                # NO está registrado —> enviar botón de confirmación
                for id_oficina, oficina in Estado.OfficesLista.items():
                    if oficina.canal.id == after.channel.id:
                        view = util.CrearEncuestaSimple([Botones.botonesEntrarOffices("Entrar a oficina", discord.ButtonStyle.green, id_oficina, member)],(60 * 5))
                        try:
                            await member.send(
                                f"Hola {member.display_name[10:]}, ¿deseas unirte a la offices?",
                                view=view
                            )
                        except discord.Forbidden:
                            canal_texto = after.channel.guild.get_channel(after.channel.id + 1)
                            if canal_texto:
                                await canal_texto.send(
                                    f"{member.mention}, ¿quieres entrar a la oficina?",
                                    view=view
                                )

async def setup(bot: commands.Bot):
    await bot.add_cog(Eventos(bot))
