import discord
from Declaraciones import Declaraciones
from Clases import Formulario

Estado = Declaraciones.EstadoGlobal()

async def agregarEstuOffices(interaction: discord.Interaction, IDOffices, Estudiante: discord.Member):
    RolesEstudiante = [rol.name for rol in Estudiante.roles]
    if any(rol in ["Staff", "Admin Staff"] for rol in RolesEstudiante):
        await interaction.response.send_message("No se puede agregar a un staff a una offices")
        return
    
    formulario = Formulario.formularioAgregarEstudiante("Agregar a un Estudiante", IDOffices,Estudiante)
    await interaction.response.send_modal(formulario)
    