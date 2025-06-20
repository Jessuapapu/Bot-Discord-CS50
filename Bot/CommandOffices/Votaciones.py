
import discord
from Declaraciones import Declaraciones
from Clases import util, Botones

Estado = Declaraciones.EstadoGlobal()

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
   
   botones = [Botones.botonesAsistencia("Estoy Presente!",discord.ButtonStyle.premium)]
   
   view = util.CrearEncuestaSimple(botones,tiempo)
   embed = util.CrearMensajeEmbed("Confirmaciones de Asistencia","Votaciones de control \n ¿Estas aun aqui?")
   
   # ephemeral es para que solo la persona que lo envio le salga el mensaje
   await interaction.response.send_message(embed=embed, view=view, ephemeral=False)     
   return

    