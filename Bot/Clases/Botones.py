import discord
from Declaraciones import Declaraciones
from Clases import util

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
        print(self.Offices.getNombreEstudiantes() and self.Offices.ControlDeVotos == 0,f"{self.Offices.getNombreEstudiantes()} and {self.Offices.ControlDeVotos}")
        if usuario in self.Offices.getNombreEstudiantes() and self.Offices.ControlDeVotos[usuario] == 0:
            self.Offices.ListaDeVotos[usuario] += 1
            self.Offices.ControlDeVotos[usuario] += 1
            Estado.OfficesLista[self.Offices.Id] = self.Offices

            await interaction_button.response.send_message("✅ Tu voto ha sido registrado.", ephemeral=True)
        else:
            await interaction_button.response.send_message("⚠ No estás registrado en esta Office o ya marcaste en la votacion", ephemeral=True)
            

class botonesEntrarOffices(botonBase):
    def __init__(self, label, style, IdOffices, Miembro):
        super().__init__(label, style)
        self.IdOffices = IdOffices
        self.miembro = Miembro  # string del ID de usuario
        self.boton.callback = self.callBack

    async def callBack(self, interaction: discord.Interaction):
        
        if str(interaction.user.name) == str(self.miembro.name):
            
            NuevoEstu = util.Estudiante(self.miembro, self.IdOffices)
            Estado.OfficesLista[self.IdOffices].Usuarios.append(NuevoEstu)
            Estado.OfficesLista[self.IdOffices].ListaDeVotos[NuevoEstu.IdUsuario] = 0
            await NuevoEstu.iniciarContador()
            await interaction.response.send_message("Has sido añadido a la oficina correctamente.")
        else:
            await interaction.response.send_message("No puedes usar este botón.", ephemeral=True)

    

