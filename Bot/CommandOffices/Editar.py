import discord
from Declaraciones import Declaraciones
from Clases import util, SelectMenus, Formulario

Estado = Declaraciones.EstadoGlobal()

async def EditarEstudiante(interaction: discord.Interaction, IDOffices, Estudiante: discord.Member):
    Estudiante = Estado.getEstudiante(Estudiante,IDOffices)
    
    if not Estudiante:
        await interaction.response.send_message("El estudiante no esta asociado el estudiante a esa offices", ephemeral=True)
        return

    formulario = Formulario.formularioEditarEstu("Edita a un estudiante",IDOffices,Estudiante)
    
    await interaction.response.send_modal(formulario)
    return
   

async def EditarOffices(interaction: discord.Interaction, IDOffices):
    ListaOffices = Estado.getOfficesTotalValues()
    headers = ["ID", "Creador", "Bloque", "Estado"]
    contenido = []
    
    for offices in ListaOffices:
        estado = ''
        if offices.Estado == 1:
            estado = "Activa"
        else:
            estado = "Revision"
            
        contenido.append([offices.Id, offices.IdUsuario, offices.bloque,estado])
    
    tabla = util.CrearTabla(headers,contenido,None)
    embed = util.CrearMensajeEmbed("Offices Listadas", f"```\n{tabla}\n```" ,discord.Color.dark_magenta())
    
    view = SelectMenus.SelectOfficesView(IDOffices)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)