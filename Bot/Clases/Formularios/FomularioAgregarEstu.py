from Clases.Formularios import FormularioBase
from discord import Member, Interaction
from Clases.EstudianteClass import Estudiante


    
class formularioAgregarEstudiante(FormularioBase.formularioBase):
    def __init__(self, title, IDOffices, DiscordMiembro : Member):
        super().__init__(title=title, IdOffices = IDOffices)
        self.DiscordMiembro = DiscordMiembro # Se trata como si fuera un estudiante, pero es solo para obtener el miembro directo del servidor 
        self.add_item(self.InputCumplimiento)

    
    async def on_submit(self, interaction:Interaction):
        
        if self.InputCumplimiento.value not in ["0.0","0.5","1.0","1.5","2.0"] or self.InputCumplimiento.value is None:
            await interaction.response.send_message("Ingrese una hora valida (0.0, 0.5, 1.0, 1.5, 2.0)",ephemeral=True)
            return
        
        EstudianteNuevo = Estudiante(self.DiscordMiembro, self.IDOffices)
        
        try:
            EstudianteNuevo.cumplimientoReal = float(self.InputCumplimiento.value)
        except:
            await interaction.response.send_message("Ingrese un cumplimiento valido",ephemeral=True)
        
        
        if self.Offices.Estado == 0:
            if self.validarDuplicados(EstudianteNuevo, self.SIG.OfficesRevision[self.Offices.Id].Usuarios):
                self.SIG.OfficesRevision[self.Offices.Id].Usuarios.append(EstudianteNuevo)
                self.SIG.OfficesRevision[self.Offices.Id].ListaDeVotos[EstudianteNuevo.IdUsuario] = 0
            else:
                await interaction.response.send_message("Estudiante Duplicado :(")
                return 
            
        elif self.Offices.Estado == 1:
            if  self.validarDuplicados(EstudianteNuevo,self.SIG.OfficesLista[self.Offices.Id].Usuarios):
                EstudianteNuevo.TiempoTotal = round(float(self.InputCumplimiento.value) * 3600)
                await EstudianteNuevo.iniciarContador()
                self.SIG.OfficesLista[self.Offices.Id].Usuarios.append(EstudianteNuevo)
                self.SIG.OfficesLista[self.Offices.Id].ListaDeVotos[EstudianteNuevo.IdUsuario] = 0
            else:
                await interaction.response.send_message("Estudiante Duplicado :(")
                return
                
        
        await interaction.response.send_message("Estudiante agregado Correctamente :)")
        
        
    def validarDuplicados(self,Estu:Estudiante,lista):
        for User in lista:
            if Estu.IdDiscord == User.IdDiscord:
                return False
        
        return True