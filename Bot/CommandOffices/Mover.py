import discord
from Declaraciones import Declaraciones
Estado = Declaraciones.EstadoGlobal()


async def Mover(interaction: discord.Interaction, canal_destino: discord.VoiceChannel, otro_miembro: discord.Member):
        autor = interaction.user
        CanalDeOrigen = otro_miembro.voice.channel if otro_miembro.voice else None
        
        IdOffices = None
        
        if not CanalDeOrigen:
           interaction.response.send_message(f"No se puede mover a {otro_miembro.display_name}", ephemeral=True)
           return
        
        if CanalDeOrigen.id not in list(Estado.CanalesDeVoz.keys()):        
           interaction.response.send_message("El canal de voz No esta en una offices Activa", ephemeral=True)
           return
           
        IdOffices = Estado.CanalesDeVoz[CanalDeOrigen.id]
        
        if otro_miembro.display_name[10:] not in Estado.OfficesLista[IdOffices].getNombreEstudiantes():
            interaction.response.send_message(f"{otro_miembro.display_name} No esta en una offices Activa", ephemeral=True)
            
        
        for miembro in [autor, otro_miembro]:
            if miembro.voice and miembro.voice.channel:
                try:
                    await miembro.move_to(canal_destino)
                except Exception as e:
                    pass     
            else:
                await interaction.response.send_message(f"{miembro.display_name} No esta en la llamada",ephemeral=True)
                return

        EstudianteEnLista = None
        
        for Estudiante in Estado.OfficesLista[IdOffices].getNombreEstudiantes():
            if Estudiante.IdUsuario == otro_miembro.display_name[10:]:
                EstudianteEnLista.iniciarContador()  
                await interaction.response.send_message("Estudiante movido correctamente",ephemeral=True)
                return

        await interaction.response.send_message("Estudiante no se ha movido correctamente!!!!!!")
