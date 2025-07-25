from discord import ui
from Declaraciones import Declaraciones
from re import match, IGNORECASE
Estado = Declaraciones.EstadoGlobal()


class formularioBase(ui.Modal):
    def __init__(self, title : str):
        super().__init__(title=title, timeout=5*60)
        
    def IniciarInput(self, label = " ", placeholder = " ", default = " ", required = False):
        Input = ui.TextInput(
            label= label,
            placeholder= placeholder, 
            default= default,
            required=required
        )
        return Input
    
    def es_formato_valido(self,texto,formato):
        patron = formato
        return match(patron, texto, IGNORECASE) is not None
    
    async def on_submit(self):
        pass

        
        
        
