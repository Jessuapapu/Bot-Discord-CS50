from discord import Interaction, Color
from Clases.Botones import BotonBase
from Clases import util
from Declaraciones import views


async def crear_boton_registro(interaction: Interaction):
    
    
    VPS = await views.viewsPersistentes()
    
    mensajeEmbed = "Holaaa, Te damos la bienvenida al servidor de discord del curso de CS50x.ni :kissing_smiling_eyes:\n\nEste es un simple paso de autentificacion!!!, solo te pediremos tu nombre completo y tu usuario del docs (el usuario con el que entras a ver los psets :nerd:)\n\n ¿tienes problemas para auntentificarte? Contacta a un staff"
    mensajeEmbed = util.CrearMensajeEmbed("Hola, esto es un simple registro :disguised_face:",mensajeEmbed, Color.gold())
    
    await interaction.response.send_message("Creando...")    
    await interaction.channel.send(embed=mensajeEmbed, view=VPS.vistaRegistro)

    