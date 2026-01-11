from Clases.Botones import BotonBase
from Declaraciones import EstadoGlobal
Estado = EstadoGlobal.EstadoGlobal()
from Clases import util
from discord import Interaction, Color

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
            
            embed = util.CrearMensajeEmbed("Registro de Asistencia","Tu Asistencia ha sido registrado :)",Color.green())
            await interaction_button.response.send_message(embed=embed, ephemeral=True)
            return
        
        embed = util.CrearMensajeEmbed("Registro de votos","⚠ No estás registrado en esta Office o ya marcaste en la votacion",Color.red())
        await interaction_button.response.send_message(embed=embed, ephemeral=True)
            