
import discord
from Declaraciones import Declaraciones

from Clases.Formularios import FormularioIniciarOffices
Estado = Declaraciones.EstadoGlobal()

async def empezar(interaction: discord.Interaction, CanalDeVoz: discord.VoiceChannel):

    form = FormularioIniciarOffices.FormularioIniciarOffices("Inicia una Offices!!!!!!",CanalDeVoz)
    
    await interaction.response.send_modal(form)
    return