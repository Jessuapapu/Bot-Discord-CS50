from Clases.Formularios import FormularioBase

from discord import Member, Interaction
from Clases import EstudianteClass


class formularioEditarEstu(FormularioBase.formularioBase):

    def __init__(self, title : str, IDOffices : str, Estudiante: EstudianteClass.Estudiante | Member | str):
        super().__init__(title=title, IdOffices=IDOffices)
        
        self.Estudiante = self.SIG.getEstudiante(Estudiante, IDOffices) if type(Estudiante != EstudianteClass.Estudiante) else Estudiante
        
        self.InputCumplimiento.label = f"Cumplimiento {self.Estudiante.cumplimientoReal}" 
        self.InputCumplimiento.default = f"{self.Estudiante.cumplimientoReal}"
        
        self.add_item(self.InputCumplimiento)
    
    async def on_submit(self, interaction: Interaction):

        anteriorHora = self.Estudiante.cumplimientoReal

        if self.InputCumplimiento.value not in ["0.0","0.5","1.0","1.5","2.0"]:
            await interaction.response.send_message("Ingrese una hora valida (0.0, 0.5, 1.0, 1.5, 2.0)",ephemeral=True)
            return
        
        Inputnumero = float(self.InputCumplimiento.value)

        self.Estudiante.cumplimientoReal = Inputnumero
        self.Estudiante.TiempoTotal = Inputnumero * 3600 if Inputnumero > 0.0 else 0
        
        
        if self.Offices.Estado == 0:
            for i,user in enumerate(self.SIG.OfficesRevision[self.Offices.Id].Usuarios):
                if user == self.Estudiante.IdUsuario:
                    self.SIG.OfficesRevision[self.Offices.Id].Usuarios[i] = self.Estudiante
                    
                    
        elif self.Offices.Estado == 1:
            for i,user in enumerate(self.SIG.OfficesLista[self.Offices.Id].Usuarios):
                if user == user == self.Estudiante.IdUsuario:
                    self.SIG.OfficesLista[self.Offices.Id].Usuarios[i] = self.Estudiante
        
        
        await interaction.response.send_message(f"Datos del estudiante han sido cambiado Correctamente: "  
                                                f"{anteriorHora} -> {Inputnumero} correctamente :)",
                                                ephemeral=True)
   