import discord
from Declaraciones import Declaraciones
import random

Estado = Declaraciones.EstadoGlobal()

async def ruletita(interaction:discord.Interaction, CanalDeVoz: discord.VoiceChannel):
    
    miembros = [
        miembro for miembro in CanalDeVoz.members
        if not any(rol.name in Estado.ListaDeRolesPermitidos for rol in miembro.roles)
    ]
    if miembros == []:
        await interaction.response.send_message(content="No hay nadie activo")
    ElElegido = random.choice(miembros)
    
    
    await interaction.response.send_message(content=f"El estudiante Selecionado es......{ElElegido.mention}")
    
    