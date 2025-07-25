import discord
from Clases.Formularios import FormularioEditarEstu, FormularioEditarOffices
from Declaraciones import Declaraciones

Estado = Declaraciones.EstadoGlobal()

async def EditarEstudiante(interaction: discord.Interaction, IDOffices, Estudiante: discord.Member):
    Estudiante = Estado.getEstudiante(Estudiante,IDOffices)
    
    if not Estudiante:
        await interaction.response.send_message("El estudiante no esta asociado el estudiante a esa offices", ephemeral=True)
        return

    formulario = FormularioEditarEstu.formularioEditarEstu("Edita a un estudiante",IDOffices,Estudiante)
    
    await interaction.response.send_modal(formulario)
    return
   

async def EditarOffices(interaction: discord.Interaction, IDOffices):
    Offices = Estado.getOffices(IDOffices)
    if not Offices:
        await interaction.response.send_message("La offices seleccionada no existe :(", ephemeral=True)
        return

    await interaction.response.send_modal(FormularioEditarOffices.formularioEditarOffices(f"Editando {IDOffices}:",IDOffices))