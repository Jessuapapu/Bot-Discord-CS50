import discord
from Formularios import FormularioBase
from Declaraciones import Declaraciones

Estado = Declaraciones.EstadoGlobal()

# Clase En desuso
# class SelectEstudianteView(discord.ui.View):
#     def __init__(self, estudiantes, IDOffices):
#         super().__init__(timeout=60)
#         self.add_item(SelectEstudiante(estudiantes, IDOffices))
        
        
class SelectOfficesView(discord.ui.View):
    def __init__(self, IDOffices):
        super().__init__(timeout=60)
        self.add_item(SelectOffices(IDOffices))


#-----------------------------------------------------------------------------------------------------------

# Clase desuso
# class SelectEstudiante(discord.ui.Select):
#     def __init__(self, estudiantes, IDOffices):
#         self.IDOffices = IDOffices
#         self.estudiantes = estudiantes

#         options = [
#             discord.SelectOption(label=estu.IdUsuario, description=f"Grupo: {estu.grupo}")
#             for estu in estudiantes
#         ]

#         super().__init__(
#             placeholder="Selecciona un estudiante para editar...",
#             min_values=1,
#             max_values=1,
#             options=options
#         )

#     async def callback(self, interaction: discord.Interaction):
#         seleccionado = self.values[0]
#         for i, estu in enumerate(self.estudiantes):
#             if estu.IdUsuario == seleccionado:
#                 modal = Formulario.formularioEditarEstu(
#                     f"Editando a {estu.IdUsuario[:45]}",
#                     self.IDOffices,
#                     estu,
#                     i
#                 )
#                 await interaction.response.send_modal(modal)
#                 break
          
            
class SelectOffices(discord.ui.Select):
    def __init__(self, IDOffices):
        self.IDOffices = IDOffices

        options = [
            discord.SelectOption(label=Office, description=f"Offices: {Office}")
            for Office in list(Estado.OfficesLista.keys()) + list(Estado.OfficesRevision.keys()) 
        ]

        super().__init__(
            placeholder="Selecciona una Offices para editar...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        seleccionado = self.values[0]
        modal = FormularioBase.formularioEditarOffices( f"Editando la offices {seleccionado}", seleccionado)
        await interaction.response.send_modal(modal)
        

"""class SelectAgregarAOffices(discord.ui.Select):
    def __init__(self, IdOffices, ListaEstudiantes):
        self.IdOffices = IdOffices
        options = ListaEstudiantes
        
        super.__init__(
            placeholder="Selecciona a un estudiante para agregar...",
            min_values=1,
            max_values=1,
            options=options
        )
        
    async def callback(self, interaction: discord.Interaction):
        seleccionado = self.values[0]
        await """