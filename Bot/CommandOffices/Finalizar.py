
import discord
from Declaraciones import Declaraciones

from Clases import util
Estado = Declaraciones.EstadoGlobal()

async def finalizar(interaction: discord.Interaction, ID):
    if len(Estado.OfficesLista) == 0 or Estado.OfficesLista[ID].Estado == 0:
        await interaction.response.send_message("No hay offices activas o la offices no esta activa")
        return

    keys = []
    mensajeEmbed = f""

    for contador in Estado.ContadoresActivos:
        Estudiante, tarea = Estado.ContadoresActivos[contador]

        if Estudiante.IdOffice == ID:
            keys.append(Estudiante.IdUsuario)
            await Estudiante.DetenerContador(tarea)
            mensajeEmbed += Estudiante.toString()
            
    await interaction.response.send_message(embed=util.CrearMensajeEmbed("Lista de Estudiantes", mensajeEmbed, discord.Color.dark_gold()))

    # Establecemos el Estado = 0 para finalizarla
    Office = Estado.OfficesLista[ID]
    Office.Estado = 0
    Estado.OfficesLista[ID] = Office 
    

    for key in keys:
        Estudiante, tarea = Estado.ContadoresActivos[key]
        Estado.ContadoresActivos.pop(Estudiante.IdUsuario)
        
    return