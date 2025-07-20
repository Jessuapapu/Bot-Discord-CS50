
import discord
from Declaraciones import Declaraciones

from Clases import OfficeClass, EstudianteClass
Estado = Declaraciones.EstadoGlobal()

async def empezar(interaction: discord.Interaction, ID, CanalDeVoz: discord.VoiceChannel, Bloque):

    miembros = [
        EstudianteClass.Estudiante(miembro, ID) for miembro in CanalDeVoz.members
        if not any(rol.name in Estado.ListaDeRolesPermitidos for rol in miembro.roles) and not miembro.bot
    ]

    if len(miembros) == 0:
        await interaction.response.send_message("No hay estudiantes conectados.")
        return
    
    for miembro in miembros:
        await miembro.iniciarContador()

    Office = OfficeClass.Offices(ID, interaction.user.display_name[8:], miembros, Bloque, CanalDeVoz)
    Estado.CanalesDeVoz[CanalDeVoz.id] = ID
    Estado.OfficesLista[ID] = Office
    await Office.Barrido50()
    
    await interaction.response.send_message("Offices Inicializada")
    return