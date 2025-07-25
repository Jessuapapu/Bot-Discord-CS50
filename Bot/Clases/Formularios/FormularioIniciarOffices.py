from Clases.Formularios import FormularioBase
from Clases.util import CrearMensajeEmbed
from Clases.OfficeClass import Offices
from Clases.EstudianteClass import Estudiante
from zoneinfo import ZoneInfo

from Declaraciones import Declaraciones
import datetime
from datetime import datetime


from discord import Interaction, VoiceChannel

Estado = Declaraciones.EstadoGlobal()

class FormularioIniciarOffices(FormularioBase.formularioBase):
    def __init__(self, title, CanalDeVoz: VoiceChannel):
        super().__init__(title=title)
        
        self.CanalDeVoz = CanalDeVoz
        
        self.informacion = self.obtenerId()
        self.InputIDOffices = self.IniciarInput("Ingrese el Id (ojo con el fomrato)!!", "Ejem: 1-S03-Martes–10-12", f"Sem-{self.informacion['Dia']}-{self.informacion['Bloque']}", True)
        
        self.InputBloque = self.IniciarInput(f"Ingrese el bloque: ", "Ejem: 8-10, 1-3", f"{self.informacion["Bloque"]}", True)
        self.InputStaff = self.IniciarInput("Ingrese los codigos del staff","Ejem: pcastillo, dknauth, ecalix, bgarcia", " ")
                           
        self.add_item(self.InputIDOffices)
        self.add_item(self.InputBloque)
        self.add_item(self.InputStaff)
            
            
    def obtenerId(self):
        informacion = {}
        dias_semana = ["lun", "mar", "mie", "jue", "vie", "sab", "dom"]

        # Obtener la hora actual en zona Nicaragua
        ahora = datetime.now(ZoneInfo("America/Managua"))

        dia_semana = dias_semana[ahora.weekday()]
        informacion["Dia"] = dia_semana

        hora_actual_24 = ahora.hour
        hora_inicio = hora_actual_24 % 12 or 12

        hora_mas_dos_24 = (hora_actual_24 + 2) % 24
        hora_fin = hora_mas_dos_24 % 12 or 12

        am_pm = "am" if hora_mas_dos_24 < 12 else "pm"

        bloque = f"{hora_inicio}-{hora_fin}{am_pm}"
        informacion["Bloque"] = bloque

        return informacion

    async def on_submit(self,interaction:Interaction):
        
        if not self.es_formato_valido(self.InputIDOffices.value, r"^\d+-(S|s)\d{2}-(lun(?:es)?|mar(?:tes)?|mie(?:rcoles)?|jue(?:ves)?|vie(?:rnes)?|sab(?:ado)?|dom(?:ingo)?)[–-](\d{1,2})-(\d{1,2})\s*([aApP][mM])$"):
            await interaction.response.send_message(f"Formato de semana no valido \n Id de Offices sugerida: Sem-{self.informacion['Dia']}-{self.informacion['Bloque']}",ephemeral = True)
            return
        
        if self.InputBloque == " " or not self.es_formato_valido(self.InputBloque.value, r"\b(\d{1,2})-(\d{1,2})\s*([aApP][mM])?\b"):
            await interaction.response.send_message(f"Ingrese un bloque Valido \n Bloque sugerido: {self.informacion['Bloque']}",ephemeral=True)
            return
        
        ID = self.InputIDOffices.value
        Bloque = self.InputBloque.value
        
        miembros = [
            Estudiante(miembro, ID) for miembro in self.CanalDeVoz.members
            if not any(rol.name in Estado.ListaDeRolesPermitidos for rol in miembro.roles) and not miembro.bot
        ]

        if len(miembros) == 0:
            await interaction.response.send_message("No hay estudiantes conectados.")
            return

        for miembro in miembros:
            await miembro.iniciarContador()

        # Retorna formateado los nombres de Staff de tal forma: ["jsolis","apalacios","bgarcia","akelly"]
        staff = self.InputStaff.value.replace(' ','').split(',') if self.InputStaff.value != "" else []
        
        Office = Offices(ID, interaction.user.display_name[8:], miembros, Bloque, self.CanalDeVoz, staff)
        Estado.CanalesDeVoz[self.CanalDeVoz.id] = ID
        Estado.OfficesLista[ID] = Office
        await Office.Barrido50()
        
        
        staffNombres = " "
        if self.InputStaff.value == "":
            staffNombres =  "No se registraron los codigos de staff!!!!"
        else:
            for Nombres in staff:
                staffNombres += Nombres + " "
            
        
        
        embed = CrearMensajeEmbed("Offices Inicializada :)", f"Datos: \n\tId -> {ID}\n\tBloque -> {Bloque}\n\tCodigos de Staff -> {staffNombres}")
        await interaction.response.send_message(embed=embed)