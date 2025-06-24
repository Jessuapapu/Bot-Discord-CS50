
import discord
from Declaraciones import Declaraciones

from Clases import util
Estado = Declaraciones.EstadoGlobal()

async def finalizar(interaction: discord.Interaction, ID):
    if len(Estado.OfficesLista) == 0 or  not Estado.OfficesLista.get(ID,None) or Estado.OfficesLista[ID].Estado == 0:
        await interaction.response.send_message("No hay offices activas o la offices no esta activa")
        return

    keys = []
    headerTabla = ["Nombre", "Grupo", "Tiempo", "votos"]
    contenidoTabla = []

    for contador in Estado.ContadoresActivos:
        Estudiante, tarea = Estado.ContadoresActivos[contador]

        if Estudiante.IdOffice == ID:
            keys.append(Estudiante.IdUsuario)
            await Estudiante.DetenerContador(tarea)
            #mensajeEmbed += f"{Estudiante.toString()} {} \n"
            
            #                      Nombre del estudiante     grupo                   horas                      votos
            contenidoTabla.append([Estudiante.IdUsuario, Estudiante.grupo, Estudiante.cumplimientoReal, Estado.OfficesLista[ID].ListaDeVotos[Estudiante.IdUsuario]])  
    
    tabla = util.CrearTabla(headerTabla,contenidoTabla)
    embed = util.CrearMensajeEmbed("Lista de Estudiantes", f"```\n{tabla}\n```", discord.Color.dark_gold())
            
    await interaction.response.send_message(embed=embed)


    # Establecemos el Estado = 0 para finalizarla
    Office = Estado.OfficesLista[ID]
    Office.Estado = 0
    Estado.OfficesLista.pop(ID)
    Estado.OfficesRevision[ID] = Office 
    

    for key in keys:
        Estudiante, tarea = Estado.ContadoresActivos[key]
        Estado.ContadoresActivos.pop(Estudiante.IdUsuario)
        
    return