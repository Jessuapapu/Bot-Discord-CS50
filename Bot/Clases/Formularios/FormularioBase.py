import discord
from Declaraciones import Declaraciones
Estado = Declaraciones.EstadoGlobal()


class formularioBase(discord.ui.Modal):
    def __init__(self, title : str):
        super().__init__(title=title, timeout=5*60)
        
    def IniciarInput(self, label = " ", placeholder = " ", default = " ", required = False):
        Input = discord.ui.TextInput(
            label= label,
            placeholder= placeholder, 
            default= default,
            required=required
        )
        return Input
    
    async def on_submit(self):
        pass

        
        
        
