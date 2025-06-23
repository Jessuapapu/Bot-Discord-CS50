
import discord
import asyncio
from Declaraciones import Declaraciones

from Clases import util
Estado = Declaraciones.EstadoGlobal()

async def empezar(interaction: discord.Interaction, ID, CanalDeVoz: discord.VoiceChannel, Bloque):

    miembros = [
        util.Estudiante(miembro, ID) for miembro in CanalDeVoz.members
        if not any(rol.name in ["Staff", "Admin Discord"] for rol in miembro.roles)
    ]

    if len(miembros) == 0:
        await interaction.response.send_message("No hay estudiantes conectados.")
        return
    
    for miembro in miembros:
        tarea = asyncio.create_task(miembro.CalcularTiempo())
        Estado.ContadoresActivos[miembro.IdUsuario] = (miembro, tarea)

    Office = util.Offices(ID, interaction.user.display_name[8:], miembros, Bloque)
    Estado.CanalesDeVoz.append(CanalDeVoz.id)
    Estado.OfficesLista[ID] = Office
    
    await interaction.response.send_message("Offices Inicializada")
    return