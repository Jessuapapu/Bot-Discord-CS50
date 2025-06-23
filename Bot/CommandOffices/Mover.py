import discord
from Declaraciones import Declaraciones
import asyncio
Estado = Declaraciones.EstadoGlobal()


async def Mover(interaction: discord.Interaction, canal_destino: discord.VoiceChannel, otro_miembro: discord.Member):
        autor = interaction.user

        errores = []

        for miembro in [autor, otro_miembro]:
            if miembro.voice and miembro.voice.channel:
                try:
                    await miembro.move_to(canal_destino)
                except Exception as e:
                    errores.append(f"No se pudo mover a {miembro.display_name}: {e}")
            else:
                errores.append(f"{miembro.display_name} no está en un canal de voz.")

        if errores:
            mensaje = "Resultado parcial:\n" + "\n".join(errores)
        else:
            if otro_miembro.display_name[10:] not in list(Estado.ContadoresActivos.keys()):
                await interaction.response.send_message("El estudiante no esta en la offices", ephemeral=True)
            mensaje = f"{autor.display_name} y {otro_miembro.display_name} fueron movidos a **{canal_destino.name}** correctamente."
            estudiante, _ = Estado.ContadoresActivos[otro_miembro.display_name[10:]]
            nueva_tarea = asyncio.create_task(estudiante.CalcularTiempo())
            Estado.ContadoresActivos[otro_miembro.display_name[10:]] = (estudiante, nueva_tarea)


        await interaction.response.send_message(mensaje)