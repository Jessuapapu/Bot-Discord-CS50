import discord
from Declaraciones import Declaraciones
from Clases import util
import asyncio

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
            

class botonesEntrarOffices(botonBase):
    def __init__(self, label, style, IdOffices, Miembro):
        super().__init__(label, style)
        self.IdOffices = IdOffices
        self.miembro = Miembro  # string del ID de usuario
        self.boton.callback = self.callBack

    async def callBack(self, interaction: discord.Interaction):
        print(interaction.user.name)
        if str(interaction.user.name) == str(self.miembro.name):
            
            NuevoEstu = util.Estudiante(self.miembro, self.IdOffices)
            Estado.OfficesLista[self.IdOffices].Usuarios.append(NuevoEstu)
            Estado.OfficesLista[self.IdOffices].ListaDeVotos[NuevoEstu.IdUsuario] = 0
            tarea = asyncio.create_task(NuevoEstu.CalcularTiempo())
            Estado.ContadoresActivos[NuevoEstu.IdUsuario] = (NuevoEstu, tarea)
            await interaction.response.send_message("Has sido añadido a la oficina correctamente.", ephemeral=True)
        else:
            await interaction.response.send_message("No puedes usar este botón.", ephemeral=True)

    

