import discord
from Clases import util
from Declaraciones import Declaraciones
Estado = Declaraciones.EstadoGlobal()

class formularioEditar(discord.ui.Modal):
    
    
    def __init__(self, title, IDOffices,Estudiante:util.Estudiante,IDEstu):
        super().__init__(title=title, timeout=180)
        self.IDOffices = IDOffices
        self.Estudiante = Estudiante
        self.IndiceEstudiante = IDEstu
        self.Input = self.IniciarInput()
        self.add_item(self.Input) 
    
    
    def IniciarInput(self):
        Input = discord.ui.TextInput(
            label=f"{self.Estudiante.IdUsuario} con cumplimiento de {self.Estudiante.cumplimientoReal}",
            placeholder=f"{self.Estudiante.cumplimientoReal}",
            default=f"{self.Estudiante.cumplimientoReal}"
        )
        return Input
    
    
    async def on_submit(self, interaction):
        try:
            Inputnumero = float(self.Input.value)
        except:
            await interaction.response.send_message("Error al tratar de obtener los datos nuevos", ephemeral=True)
        
        
        if Estado.OfficesRevision[self.IDOffices].Usuarios[self.IndiceEstudiante].cumplimientoReal == Inputnumero:
            await interaction.response.send_message("Datos obtenidos del estudiante iguales a los originales", ephemeral=True)
            return
        
        Estado.OfficesRevision[self.IDOffices].Usuarios[self.IndiceEstudiante].cumplimientoReal = Inputnumero
        
        await interaction.response.send_message(f"Datos del estudiante {self.Estudiante.IdUsuario} han sido cambiado correctamente :)", ephemeral=True)
   
   