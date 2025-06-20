import discord
from Declaraciones import Declaraciones

Estado = Declaraciones.EstadoGlobal()

class botonBase:
    def __init__(self, label: str, style: discord.ButtonStyle):
        self.boton = discord.ui.Button(label=label, style=style)
        self.boton.callback = self.callBack

    async def callBack(self, interaction_button: discord.Interaction):
        pass


class botonesAsistencia(botonBase):
    def __init__(self, label, style, IdOffices):
        super().__init__(label, style)

        # Asociar el boton a una offices
        self.Offices = Estado.OfficesLista[IdOffices]
        self.boton.callback = self.callBack

    async def callBack(self, interaction_button: discord.Interaction):
        usuario = interaction_button.user.display_name[10:]
        
        # Valida si el usuario está en la lista de estudiantes de la office
        if usuario in self.Offices.getEstudiantes():
            self.Offices.ListaDeVotos[usuario] += 1
            Estado.OfficesLista[self.Offices.Id] = self.Offices

            await interaction_button.response.send_message("✅ Tu voto ha sido registrado.", ephemeral=True)
        else:
            await interaction_button.response.send_message("⚠ No estás registrado en esta Office.", ephemeral=True)

