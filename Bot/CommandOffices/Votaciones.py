
import discord
from Clases.Botones import BotonesAsistencia
from Declaraciones import EstadoGlobal
from Clases import util

Estado = EstadoGlobal.EstadoGlobal()

async def votacion(interaction:discord.Interaction,ID,tiempo):
   """
   # Crear los botones para las opciones
   boton = discord.ui.Button(label="Estoy presente", style=discord.ButtonStyle.primary)
   
   # Crear la vista para mostrar los botones
   view = discord.ui.View()
   view.add_item(boton)
   message = "Estoy Presente :)\n\n"
   
   message += f"Si : {boton.label}"
      
   await interaction.response.send_message(message, view=view, ephemeral=False)
   """
   
   botones = [BotonesAsistencia.botonesAsistencia("Estoy Presente!",discord.ButtonStyle.success,ID)]
   
   offices = Estado.OfficesLista[ID]
   offices.iniciarContadorDeVotos()
   view = util.CrearEncuestaSimple(botones,tiempo)
   embed = util.CrearMensajeEmbed(" :black_nib: ```          - Confirmaciones de Asistencia -          ``` :black_bird: ","Votaciones de control \n ¿Estas aun aqui?:face_with_raised_eyebrow:")
   imagenEmbed = discord.File("./Bot/Plantilla/RegistroDeAsistencia.png")
   embed.set_image(url='attachment://imagen_embed.png')
   await interaction.response.defer(ephemeral=False,thinking=True)
   
   # ephemeral es para que solo la persona que lo envio le salga el mensaje
   await interaction.followup.send(embed=embed, view=view, file=imagenEmbed, ephemeral=False)     
   return

    