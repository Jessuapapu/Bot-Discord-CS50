import discord
from Clases import util
from Declaraciones import Declaraciones
Estado = Declaraciones.EstadoGlobal()

class formularioEditarEstu(discord.ui.Modal):

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
        anterior = Estado.OfficesRevision[self.IDOffices].Usuarios[self.IndiceEstudiante].cumplimientoReal
        try:
            Inputnumero = float(self.Input.value)
            
        except:
            await interaction.response.send_message("Error al tratar de obtener los datos nuevos", ephemeral=True)
            return
        
        
        if Estado.OfficesRevision[self.IDOffices].Usuarios[self.IndiceEstudiante].cumplimientoReal == Inputnumero:
            await interaction.response.send_message("Datos obtenidos del estudiante iguales a los originales", ephemeral=True)
            return
        
        Estado.OfficesRevision[self.IDOffices].Usuarios[self.IndiceEstudiante].cumplimientoReal = Inputnumero
        
        await interaction.response.send_message(f"Datos del estudiante {self.Estudiante.IdUsuario} han sido cambiado de {anterior} a {Inputnumero} correctamente :)", ephemeral=True)
   

class formularioEditarOffices(discord.ui.Modal):
    def __init__(self, title, IDOffices):
        super().__init__(title=title, timeout=180)
        self.IDOffices = IDOffices
        self.Offices = None
        
        # Tiene que entrar en uno
        try:
            self.Offices = Estado.OfficesLista[self.IDOffices]
        except:
            self.Offices = Estado.OfficesRevision[self.IDOffices]
            
        self.Input1 = self.IniciarInput()
        self.Input2 = self.IniciarInput2()
        self.add_item(self.Input1)
        self.add_item(self.Input2) 
        
    def IniciarInput(self):
        Input = discord.ui.TextInput(
            label=f"Id de offices: {self.IDOffices}",
            placeholder=f"{self.IDOffices}",
            default=f"{self.IDOffices}"
        )
        return Input
    
    def IniciarInput2(self):
        Input = discord.ui.TextInput(
            label=f"Bloque de la offices : {self.Offices.bloque}",
            placeholder=f"formato aceptado 10-12, 1-3, 3-5",
            default=f"{self.Offices.bloque}"
        )
        return Input
    
    async def on_submit(self, interaction):
        
        if self.Input2.value not in ["10-12","1-3","3-5","10 - 12","1 - 3","3 - 5"]:
            await interaction.response.send_message("Error en el formato de las Horas")
            return
        
        
        if self.Input1.value in list(Estado.OfficesLista.keys()) + list(Estado.OfficesRevision.keys()) and not self.IDOffices:
            await interaction.response.send_message("Ya existe una offices con ese nombre")
        
        
        Offices = None
        try:
            Offices = Estado.OfficesLista[self.IDOffices]
            del Estado.OfficesLista[self.IDOffices]
        except:
            Offices = Estado.OfficesRevision[self.IDOffices]
            del Estado.OfficesRevision[self.IDOffices]
            
            
        Offices.Id = self.Input1.value
        Offices.bloque = self.Input2.value
        
        Estado.OfficesRevision[Offices.Id] = Offices
        
        await interaction.response.send_message("Offices editada Correctamente :)")
        
            
        
    
    
    
    