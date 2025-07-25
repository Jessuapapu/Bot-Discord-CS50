import discord
from Declaraciones import Declaraciones
from Clases.Formularios import FomularioAgregarEstu

Estado = Declaraciones.EstadoGlobal()

async def agregarEstuOffices(interaction: discord.Interaction, IDOffices, Estudiante: discord.Member):
    
    RolesEstudiante = [rol.name for rol in Estudiante.roles]
    
    # valida si es un bot o un staff
    if any(rol in Estado.ListaDeRolesPermitidos for rol in RolesEstudiante) or Estudiante.bot:
        await interaction.response.send_message("No se pueden agregar a un staff o aun bot a una offices")
        return
    
    CanalDeVoz = Estudiante.voice.channel if Estudiante.voice else None
    
    
    # Valida si esta conectado o si esta en un canal con una offices
    if not CanalDeVoz or CanalDeVoz.id not in Estado.getKeyCanalesDeVoz():
        await interaction.response.send_message("El estudiante no esta en un canal de voz o no esta conectado a una offices :(",ephemeral=True)
        return
    
    formulario = FomularioAgregarEstu.formularioAgregarEstudiante("Agregar a un Estudiante", IDOffices,Estudiante)
    await interaction.response.send_modal(formulario)