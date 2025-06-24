import discord
import asyncio
from Declaraciones import Declaraciones
from Clases import util, SelectMenus

Estado = Declaraciones.EstadoGlobal()

async def EditarEstudiante(interaction: discord.Interaction, IDOffices):
    headerTabla = ["Nombre", "Grupo", "Tiempo", "votos"]
    contenidoTabla = []
    Contents = None
    try:
        Contents = Estado.OfficesRevision[IDOffices]
    except:
        Contents = Estado.OfficesLista[IDOffices]
    
    
    for estu in Contents.Usuarios:
        contenidoTabla.append([
            estu.IdUsuario,
            estu.grupo,
            estu.cumplimientoReal,
            Contents.ListaDeVotos[estu.IdUsuario]
        ])

    tabla = util.CrearTabla(headerTabla, contenidoTabla)
    embed = util.CrearMensajeEmbed(
        "Estudiantes disponibles para editar",
        f"Selecciona uno del menú.\n```\n{tabla}\n```",
        discord.Color.dark_gold()
    )

    view = SelectMenus.SelectEstudianteView(Contents.Usuarios, IDOffices)
    await interaction.response.send_message(embed=embed, view=view)


async def EditarOffices(interaction: discord.Interaction, IDOffices):
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
    
    view = SelectMenus.SelectOfficesView(IDOffices)
    await interaction.response.send_message(embed=embed, view=view)