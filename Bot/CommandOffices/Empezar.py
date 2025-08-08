
import discord
from Declaraciones import EstadoGlobal

from Clases.Formularios import FormularioIniciarOffices
Estado = EstadoGlobal.EstadoGlobal()

async def empezar(interaction: discord.Interaction, CanalDeVoz: discord.VoiceChannel):

    form = FormularioIniciarOffices.FormularioIniciarOffices("Inicia una Offices!!!!!!",CanalDeVoz)
    
    await interaction.response.send_modal(form)
    return