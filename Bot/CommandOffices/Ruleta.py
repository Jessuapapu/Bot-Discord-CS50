import discord
from Clases import util
from Declaraciones import Declaraciones
from PIL import Image, ImageDraw, ImageFont
import random, os

Estado = Declaraciones.EstadoGlobal()

async def ruletita(interaction:discord.Interaction, CanalDeVoz: discord.VoiceChannel):
    
    miembros = [
        miembro for miembro in CanalDeVoz.members
        if not any(rol.name in ["Staff", "Admin Discord"] for rol in miembro.roles)
    ]
    if miembros == []:
        await interaction.response.send_message(content="No hay nadie activo")
    ElElegido = random.choice(miembros)

    ruta_base = os.path.dirname(os.path.dirname(__file__))
    ruta_plantillas = os.path.join(ruta_base, 'Plantilla')
    image = Image.open(ruta_plantillas + "/PlantillaRuleta.jpg")

    
    draw = ImageDraw.Draw(image)

    ancho_imagen, alto_imagen = image.size
    
    # Texto que vas a poner
    fuente = ImageFont.truetype("arial.ttf", 500)
    texto = ElElegido.display_name[10:]

    # Medidas del texto con textbbox
    bbox = draw.textbbox((0, 0), texto, font=fuente)
    ancho_texto = bbox[2] - bbox[0]
    alto_texto = bbox[3] - bbox[1]

    # Posición centrada
    posicion = ((ancho_imagen - ancho_texto) / 2, (alto_imagen - alto_texto + 50)/2)

    # Añadir texto a la imagen
    draw.text(posicion, texto, font=fuente, fill=(255, 255, 255))

    # Guarda la imagen modificada
    image.save(ruta_plantillas + "/imagen_con_texto.jpg")
    
    await interaction.response.send_message(content=f"El estudiante Selecionado es......{ElElegido.mention}",file = discord.File(ruta_plantillas + "/imagen_con_texto.jpg"))
    os.remove(ruta_plantillas + "/imagen_con_texto.jpg")
    
    