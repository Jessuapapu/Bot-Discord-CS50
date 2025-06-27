import discord
from Declaraciones import Declaraciones
from Clases import util, SelectMenus

Estado = Declaraciones.EstadoGlobal()

async def agregarEstuOffices(interaction: discord.Interaction, IDOffices):
    ListaOffices = []
    
    for oh in Estado.OfficesLista:
        ListaOffices.append(Estado.OfficesLista[oh])
    for oh in Estado.OfficesRevision:
        ListaOffices.append(Estado.OfficesRevision[oh])
    
    
    headers = ["ID", "Creador", "Hora", "Bloque", "Estado"]
    contenido = []
    
    for offices in ListaOffices:
        estado = ''
        if offices.Estado == 1:
            estado = "Activa"
        else:
            estado = "Revision"
            
        contenido.append([offices.Id, offices.IdUsuario, offices.HoraCreacion, offices.bloque,estado])
    
    tabla = util.CrearTabla(headers,contenido)
    embed = util.CrearMensajeEmbed("Offices Listadas", f"```\n{tabla}\n```" ,discord.Color.dark_magenta())
    
    view = SelectMenus.SelectOfficesView(IDOffices)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)