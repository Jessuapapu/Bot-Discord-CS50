import discord
from Declaraciones import Declaraciones
from Bot.Clases.Formularios import FormularioBase

Estado = Declaraciones.EstadoGlobal()


async def borrar(Interaction: discord.Interaction, IdOffices, Estudiante:discord.Member):
    Selecionado = Estado.getEstudiante(Estudiante,IdOffices)
    
    if not Selecionado:
        await Interaction.response.send_message("El Estudiante no esta registrado en esas offices",ephemeral=True)
        return
    
    
    
    await Interaction.response.send_message("Estudiante eliminado correctamnete >:)", ephemeral=True)
    return