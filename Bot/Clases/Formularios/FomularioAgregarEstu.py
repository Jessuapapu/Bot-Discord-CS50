from Clases.Formularios import FormularioBase
from Declaraciones import Declaraciones
from discord import Member, Interaction
from Clases.EstudianteClass import Estudiante
Estado = Declaraciones.EstadoGlobal()

    
class formularioAgregarEstudiante(FormularioBase.formularioBase):
    def __init__(self, title, IDOffices, DiscordMiembro : Member):
        super().__init__(title=title)
        self.IDOffices = IDOffices
        self.Offices = Estado.getOffices(IDOffices)
        self.DiscordMiembro = DiscordMiembro # Se trata como si fuera un estudiante, pero es solo para obtener el miembro directo del servidor
        
        # Tiene que entrar en uno / Refactorizado :)
        # try:
        #     self.Offices = Estado.OfficesLista[self.IDOffices]
        # except:
        #     self.Offices = Estado.OfficesRevision[self.IDOffices]
            
        #self.InputNombreEstudiante = self.IniciarInput("Nombre del estudiante", f"", None)
        #self.InputGrupoEstudiante = self.IniciarInput("Grupo del estudiante (Solo la letra)", f"", None)
        self.InputCumplimientoEstu = self.IniciarInput("Cumplimiento en Horas","Si esta activa se calcula el tiempo",0.0,True)

        #self.add_item(self.InputNombreEstudiante)
        #self.add_item(self.InputGrupoEstudiante)
        self.add_item(self.InputCumplimientoEstu)

    
    async def on_submit(self, interaction:Interaction):
        
        if self.InputCumplimientoEstu.value not in ["0.0","0.5","1.0","1.5","2.0"] or self.InputCumplimientoEstu.value is None:
            await interaction.response.send_message("Ingrese una hora valida (0.0, 0.5, 1.0, 1.5, 2.0)",ephemeral=True)
            return
        
        # Innecesario, pero de una forma de colocar el nombre (Refactorizado)
        """if self.InputNombreEstudiante is None:
            await interaction.response.send_message("Ingrese un Nombre Valido",ephemeral=True)
            return"""
        
        # Innecesario, pero es otra forma de colocar el grupo (Refactorizado)
        """if self.InputGrupoEstudiante.value.lower() not in ["a","b","c","d","e","f","g","h","i"] or self.InputGrupoEstudiante is None:
            await interaction.response.send_message("Ingrese solo la letra del grupo A, B, C, D, E, F, G, H, I",ephemeral=True)
            return"""
        
            
        EstudianteNuevo = Estudiante(self.DiscordMiembro,self.IDOffices)
        EstudianteNuevo.cumplimientoReal = float(self.InputCumplimientoEstu.value)
        
        
        if self.Offices.Estado == 0:
            if self.validarDuplicados(EstudianteNuevo,Estado.OfficesRevision[self.Offices.Id].Usuarios):
                Estado.OfficesRevision[self.Offices.Id].Usuarios.append(EstudianteNuevo)
                Estado.OfficesRevision[self.Offices.Id].ListaDeVotos[EstudianteNuevo.IdUsuario] = 0
            else:
                await interaction.response.send_message("Estudiante Duplicado :(")
                return 
            
        elif self.Offices.Estado == 1:
            if  self.validarDuplicados(EstudianteNuevo,Estado.OfficesLista[self.Offices.Id].Usuarios):
                EstudianteNuevo.TiempoTotal = round(float(self.InputCumplimientoEstu.value) * 3600)
                await EstudianteNuevo.iniciarContador()
                Estado.OfficesLista[self.Offices.Id].Usuarios.append(EstudianteNuevo)
                Estado.OfficesLista[self.Offices.Id].ListaDeVotos[EstudianteNuevo.IdUsuario] = 0
            else:
                await interaction.response.send_message("Estudiante Duplicado :(")
                return
                
        
        await interaction.response.send_message("Estudiante agregado Correctamente :)")
        
        
    def validarDuplicados(self,Estu:Estudiante,lista):
        for User in lista:
            if Estu.IdDiscord == User.IdDiscord:
                return False
        
        return True