import discord
from . import Formulario



class SelectEstudianteView(discord.ui.View):
    def __init__(self, estudiantes, IDOffices):
        super().__init__(timeout=60)
        self.add_item(SelectEstudiante(estudiantes, IDOffices))


class SelectEstudiante(discord.ui.Select):
    def __init__(self, estudiantes, IDOffices):
        self.IDOffices = IDOffices
        self.estudiantes = estudiantes

        options = [
            discord.SelectOption(label=estu.IdUsuario, description=f"Grupo: {estu.grupo}")
            for estu in estudiantes
        ]

        super().__init__(
            placeholder="Selecciona un estudiante para editar...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        seleccionado = self.values[0]
        for i, estu in enumerate(self.estudiantes):
            if estu.IdUsuario == seleccionado:
                modal = Formulario.formularioEditar(
                    f"Editando a {estu.IdUsuario}",
                    self.IDOffices,
                    estu,
                    i
                )
                await interaction.response.send_modal(modal)
                break

