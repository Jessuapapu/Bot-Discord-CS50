from discord import ui
from re import match, IGNORECASE

import datetime
from datetime import datetime
from zoneinfo import ZoneInfo

from Declaraciones import EstadoGlobal
Estado = EstadoGlobal.EstadoGlobal()

class formularioBase(ui.Modal):
    def __init__(self, title : str, IdOffices : str | None = None ):
        super().__init__(title=title, timeout=5*60)
        
        # Valores importantes
        self.Offices = Estado.getOffices(IdOffices) if IdOffices else None
        self.IdOffices = IdOffices
        self.SIG = Estado
        self.informacion = self.obtenerId()
        
        # Inputs genericos 
        # para ser usados tienen que ser agregados al view del modal
        self.InputStaff = self.IniciarInput("Ingrese los codigos del staff","Ejem: pcastillo, dknauth, ecalix, bgarcia", " ")
        self.InputBloque = self.IniciarInput(f"Ingrese el bloque: ", "Ejem: 8-10, 1-3", f"{self.informacion['Bloque']}", True)
        self.InputCumplimiento = self.IniciarInput(f"Cumplimiento: ","Rango aceptado: 0.0 - 2.0", "0.0")
         
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

    def obtenerId(self):
        informacion = {}
        dias_semana = ["lun", "mar", "mie", "jue", "vie", "sab","dom"]

        # Obtener la hora actual en zona Nicaragua
        ahora = datetime.now(ZoneInfo("America/Managua"))

        dia_semana = dias_semana[ahora.weekday()]
        informacion["Dia"] = dia_semana

        hora_actual_24 = ahora.hour
        hora_inicio = hora_actual_24 % 12 or 12

        hora_mas_dos_24 = (hora_actual_24 + 2) % 24
        hora_fin = hora_mas_dos_24 % 12 or 12

        # am_pm = "am" if hora_mas_dos_24 < 12 else "pm"

        # bloque = f"{hora_inicio}-{hora_fin}{am_pm}"
        bloque = f"{hora_inicio}-{hora_fin}"
        informacion["Bloque"] = bloque

        return informacion       
        
    
