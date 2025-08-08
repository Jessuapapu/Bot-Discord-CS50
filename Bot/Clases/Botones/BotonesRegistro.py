from discord import Interaction, ui, ButtonStyle
from Clases.Formularios import FormuarioFormatoEstu

    
# Boton encargado de hacer la auto registro del estudiante y colocarle el fomrato correspodiente
class botonesRegistro(ui.Button):
    def __init__(self, label="Registrate ahora Mismo!!!", style=ButtonStyle.green):
        super().__init__(label=label, style=style, custom_id="BotonRegistro")

    async def callback(self, interaction: Interaction):
        formulario = FormuarioFormatoEstu.FormularioFormato("Registro para Autentificacion")
        
        autorRoles = [rol.name for rol in interaction.user.roles]
        
        # comentariado para pruebas KAJKASJKSJ
        # if any("student" or "staff" in rol.lower() for rol in autorRoles):
        #     await interaction.response.send_message("Ya estas registrado o eres un staff jeje pillo :nerd:",ephemeral=True)
        #     return
            
        await interaction.response.send_modal(formulario)