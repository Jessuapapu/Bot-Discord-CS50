from Clases.Formularios import FormularioBase
from Clases.util import CrearMensajeEmbed
from Clases.OfficeClass import Offices
from Clases.EstudianteClass import Estudiante


from Declaraciones import Declaraciones
import datetime
import re
from discord import Interaction, VoiceChannel

Estado = Declaraciones.EstadoGlobal()

class FormularioIniciarOffices(FormularioBase.formularioBase):
    def __init__(self, title, CanalDeVoz: VoiceChannel):
        super().__init__(title=title)
        
        self.CanalDeVoz = CanalDeVoz
        
        self.informacion = self.obtenerId()
        self.InputIDOffices = self.IniciarInput(f"Sem-{self.informacion['Dia']}-{self.informacion['Bloque']}", "Ejem: 1-S03-Martes–10-12", "", True)
        
        self.InputBloque = self.IniciarInput(f"Ingrese el bloque: {self.informacion["Bloque"]}","Ejem: 8-10, 1-3"," ", True)
        self.InputStaff = self.IniciarInput("Ingrese los codigos del staff","Ejem: pcastillo, dknauth, ecalix, bgarcia", " ")
                           
        self.add_item(self.InputIDOffices)
        self.add_item(self.InputBloque)
        self.add_item(self.InputStaff)
            
            
    def obtenerId(self):
        informacion = {}
        dias_semana = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]
        informacion["Dia"] = dias_semana[datetime.date.today().weekday()]
        
        hora = (int(datetime.datetime.now().strftime("%H")) % 12)
        AmyPm = "am" if int(datetime.datetime.now().strftime("%H")) + 2 <= 12 else "pm"
        horaMasDos = hora + 2 if int(datetime.datetime.now().strftime("%H")) + 2 < 12 else (hora + 2) % 12

        # Hora(en el momento) - horaMasDos(Am o Pm) <- el Am o Pm va junto
        # ejemplo -> hora-horaMAsDosAm -> 8-10Am
        bloque = str(str(hora) + "-" + str(horaMasDos) + AmyPm)
        
        informacion["Bloque"] = bloque
        
        # informacion[semana] = SEMANA DEL SISTEMA (aun por hacer)
        return informacion
    
    def es_formato_valido(self,texto,formato):
        patron = formato
        return re.match(patron, texto, re.IGNORECASE) is not None
    
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
        staff = self.InputStaff.value.replace(' ','').split(',') if self.InputStaff.value != " " else []
        
        Office = Offices(ID, interaction.user.display_name[8:], miembros, Bloque, self.CanalDeVoz, staff)
        Estado.CanalesDeVoz[self.CanalDeVoz.id] = ID
        Estado.OfficesLista[ID] = Office
        await Office.Barrido50()
        staffNombres = ""
        print(self.InputStaff.value)
        
        if self.InputStaff.value is not "":
            for Nombres in staff:
                staffNombres += Nombres + " "
        else:
            staffNombres =  "No se registraron los codigos de staff!!!!"
        
        
        embed = CrearMensajeEmbed("Offices Inicializada :)", f"Datos: \n\tId -> {ID}\n\tBloque -> {Bloque}\n\tCodigos de Staff -> {staffNombres}")
        await interaction.response.send_message(embed=embed)