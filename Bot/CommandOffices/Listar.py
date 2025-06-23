import discord
from Declaraciones import Declaraciones
from Clases import util
Estado = Declaraciones.EstadoGlobal()


async def ListaOffices(interaction:discord.Interaction):
    ListaOffices = []
    
    for oh in Estado.OfficesLista:
        ListaOffices.append(Estado.OfficesLista[oh])
    for oh in Estado.OfficesRevision:
        ListaOffices.append(Estado.OfficesRevision[oh])
    
    
    headers = ["ID", "Creador", "Hora de Creacion", "Bloque", "Estado"]
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
    await interaction.response.send_message(embed=embed)
    
    
async def ListaEstudiantes(interaction:discord.Interaction, ID):
    listaEstu = []
    try:
        listaEstu = Estado.OfficesLista[ID]
    except:
        try:
            listaEstu = Estado.OfficesRevision[ID]
        except:
            await interaction.response.send_message("Error al obtener la lista de usuarios de la offices indicada o no existe",ephemeral=True)
            return
        
    headerTabla = ["Nombre", "Grupo", "Cumplimiento", "votos"]
    contenidoTabla = []
    for Estudiante in listaEstu.Usuarios:
        contenidoTabla.append([Estudiante.IdUsuario, Estudiante.grupo, Estudiante.cumplimientoReal, listaEstu.ListaDeVotos[Estudiante.IdUsuario]]) 
        
    tabla = util.CrearTabla(headerTabla,contenidoTabla)
    embed = util.CrearMensajeEmbed("Lista de Estudiantes", f"```\n{tabla}\n```", discord.Color.dark_gold())

    await interaction.response.send_message(embed=embed)
    
    