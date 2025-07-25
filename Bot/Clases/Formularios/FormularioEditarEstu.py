from Clases.Formularios import FormularioBase
from Declaraciones import Declaraciones
from discord import Member, Interaction
from Clases import EstudianteClass
Estado = Declaraciones.EstadoGlobal()

class formularioEditarEstu(FormularioBase.formularioBase):

    def __init__(self, title : str, IDOffices : str, Estudiante: EstudianteClass.Estudiante | Member | str):
        super().__init__(title=title)
        self.IDOffices = IDOffices
        self.Estudiante = Estado.getEstudiante(Estudiante, IDOffices) if type(Estudiante) is not EstudianteClass.Estudiante else Estudiante
        self.Offices = Estado.getOffices(IDOffices)
        
        # # Tiene que entrar en uno (Refactorizado)
        # if self.IDOffices in Estado.getKeyOfficesLista():
        #     self.Offices = Estado.OfficesLista[self.IDOffices]
        # else:
        #     self.Offices = Estado.OfficesRevision[self.IDOffices]

        self.InputNombreEstudiante = self.IniciarInput("Nombre del estudiante", f"{self.Estudiante.IdUsuario}", self.Estudiante.IdUsuario)
        self.InputGrupoEstudiante = self.IniciarInput("Grupo del estudiante (Solo la letra)", f"{self.Estudiante.grupo[6]}", self.Estudiante.grupo[6])
        self.InputCumplimiento = self.IniciarInput(f"Cumplimiento {self.Estudiante.cumplimientoReal}","Rango aceptado: 0.0 - 2.0",f"{self.Estudiante.cumplimientoReal}")
        
        self.add_item(self.InputNombreEstudiante)
        self.add_item(self.InputGrupoEstudiante)
        self.add_item(self.InputCumplimiento)
    
    async def on_submit(self, interaction: Interaction):
        
        anteriorNombre = self.Estudiante.IdUsuario
        anteriorHora = self.Estudiante.cumplimientoReal
        anteriorGrupo = self.Estudiante.grupo
        
        if self.InputCumplimiento.value not in ["0.0","0.5","1.0","1.5","2.0"]:
            await interaction.response.send_message("Ingrese una hora valida (0.0, 0.5, 1.0, 1.5, 2.0)",ephemeral=True)
            return
        
        if self.InputGrupoEstudiante.value is None or self.InputGrupoEstudiante.value.lower() not in ["a","b","c","d","e","f","g","h","i"]:
            await interaction.response.send_message("Ingrese solo la letra del grupo A, B, C, D, E, F, G, H, I",ephemeral=True)
            return
        
        try:
            Inputnumero = float(self.InputCumplimiento.value)    
        except:
            await interaction.response.send_message("Error al tratar de obtener los datos nuevos, formato equivocado", ephemeral=True)
            return
        
        
        if Inputnumero > 2.0:
            await interaction.response.send_message("Sobre exceden el tiempo permitido", ephemeral=True)
            return
        
        self.Estudiante.IdUsuario = self.InputNombreEstudiante.value
        self.Estudiante.grupo = f"Grupo {self.InputGrupoEstudiante.value.upper()}"
        self.Estudiante.cumplimientoReal = Inputnumero
        self.Estudiante.TiempoTotal = Inputnumero * 3600 if Inputnumero > 0.0 else 0
        
        if self.Offices.Estado == 0:
            for i,user in enumerate(Estado.OfficesRevision[self.Offices.Id].Usuarios):
                if user == anteriorNombre:
                    Estado.OfficesRevision[self.Offices.Id].Usuarios[i] = self.Estudiante
                    
        elif self.Offices.Estado == 1:
            for i,user in enumerate(Estado.OfficesLista[self.Offices.Id].Usuarios):
                if user == anteriorNombre:
                    Estado.OfficesLista[self.Offices.Id].Usuarios[i] = self.Estudiante
        
        await interaction.response.send_message(f"Datos del estudiante han sido cambiado Correctamente, {anteriorNombre} -> {self.Estudiante.IdUsuario}, {anteriorHora} -> {Inputnumero}, {anteriorGrupo} -> Grupo {self.InputGrupoEstudiante} correctamente :)", ephemeral=True)
   