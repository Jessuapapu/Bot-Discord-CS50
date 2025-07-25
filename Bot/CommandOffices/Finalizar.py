import discord
from Declaraciones import Declaraciones

from Clases import util
Estado = Declaraciones.EstadoGlobal()

async def finalizar(interaction: discord.Interaction, ID):
    if len(Estado.OfficesLista) == 0 or not Estado.OfficesLista.get(ID,None) or Estado.OfficesLista[ID].Estado == 0:
        await interaction.response.send_message("No hay offices activas o la offices no esta activa",ephemeral=True)
        return

    
    headerTabla = ["Nombre", "Grupo", "Tiempo", "votos"]
    contenidoTabla = []

    for Estudiante in Estado.OfficesLista[ID].Usuarios:
        await Estudiante.DetenerContador()
              
        #                      Nombre del estudiante      grupo                   horas                      votos
        contenidoTabla.append([Estudiante.IdUsuario, Estudiante.grupo, Estudiante.cumplimientoReal, Estado.OfficesLista[ID].ListaDeVotos[Estudiante.IdUsuario]])  


    # Establecemos el Estado = 0 para finalizarla
    Office = Estado.OfficesLista[ID]
    Office.Estado = 0
    
    del Estado.OfficesLista[ID]
    del Estado.CanalesDeVoz[Office.canal.id]
    Estado.OfficesRevision[ID] = Office 

    tabla = util.CrearTabla(headerTabla,contenidoTabla,None)
    embed = util.CrearMensajeEmbed("Lista de Estudiantes", f"El tiempo es total en horas\n```\n{tabla}\n```", discord.Color.dark_gold())
            
    await interaction.response.send_message(embed=embed)
 
        
    return