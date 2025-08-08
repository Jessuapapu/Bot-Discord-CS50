from Clases.Botones import BotonBase
from Declaraciones import EstadoGlobal
Estado = EstadoGlobal.EstadoGlobal()
from discord import Interaction

class botonesAsistencia(BotonBase.botonBase):
    def __init__(self, label, style, IdOffices):
        super().__init__(label, style)

        # Asociar el boton a una offices
        self.Offices = Estado.OfficesLista[IdOffices]
        self.boton.callback = self.callBack

    async def callBack(self, interaction_button: Interaction):
        usuario = interaction_button.user.display_name[10:]
        
        # Valida si el usuario está en la lista de estudiantes de la office
        if usuario in self.Offices.getNombreEstudiantes() and self.Offices.ControlDeVotos[usuario] == 0:
            self.Offices.ListaDeVotos[usuario] += 1
            self.Offices.ControlDeVotos[usuario] += 1
            Estado.OfficesLista[self.Offices.Id] = self.Offices

            await interaction_button.response.send_message("✅ Tu voto ha sido registrado.", ephemeral=True)
        else:
            await interaction_button.response.send_message("⚠ No estás registrado en esta Office o ya marcaste en la votacion", ephemeral=True)
            