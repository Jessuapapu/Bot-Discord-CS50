
import discord
from Clases.Botones import BotonBase
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
   
   botones = [BotonBase.botonesAsistencia("Estoy Presente!",discord.ButtonStyle.success,ID)]
   offices = Estado.OfficesLista[ID]
   offices.iniciarContadorDeVotos()
   view = util.CrearEncuestaSimple(botones,tiempo)
   embed = util.CrearMensajeEmbed("Confirmaciones de Asistencia","Votaciones de control \n ¿Estas aun aqui?")
   
   # ephemeral es para que solo la persona que lo envio le salga el mensaje
   await interaction.response.send_message(embed=embed, view=view, ephemeral=False)     
   return

    