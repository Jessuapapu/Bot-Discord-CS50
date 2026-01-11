from Clases.Formularios import FormularioBase
from Clases.util import CrearMensajeEmbed
from Clases.OfficeClass import Offices
from Clases.EstudianteClass import Estudiante

from discord import Interaction, VoiceChannel


class FormularioIniciarOffices(FormularioBase.formularioBase):
    def __init__(self, title, CanalDeVoz: VoiceChannel):
        super().__init__(title=title)
        
        self.CanalDeVoz = CanalDeVoz
        self.InputIDOffices = self.IniciarInput("Ingrese el Id (ojo con el formato)!!", "Ejem: 1-S03-Martes ", f"Sem-{self.informacion['Dia']}", True)
                        
        self.add_item(self.InputIDOffices)
        self.add_item(self.InputBloque)
        self.add_item(self.InputStaff)

    async def on_submit(self,interaction:Interaction):
        
        if not self.es_formato_valido(self.InputIDOffices.value, r"^\d+-(S|s)\d{2}-(lun(?:es)?|mar(?:tes)?|mie(?:rcoles)?|jue(?:ves)?|vie(?:rnes)?|sab(?:ado)?|dom(?:ingo)?)$"):
            await interaction.response.send_message(f"Formato de semana no valido \n Id de Offices sugerida: Sem-{self.informacion['Dia']}",ephemeral = True)
            return
        
        if not self.es_formato_valido(self.InputBloque.value, r"\b(\d{1,2})-(\d{1,2})\b"):
            await interaction.response.send_message(f"Ingrese un bloque Valido \n Bloque sugerido: {self.informacion['Bloque']}",ephemeral=True)
            return
        
        ID = f"{self.InputIDOffices.value}-{self.InputBloque.value}"
        Bloque = self.InputBloque.value
        
        miembros = [
            Estudiante(miembro, ID) for miembro in self.CanalDeVoz.members
            if not any(rol.name in self.SIG.ListaDeRolesPermitidos for rol in miembro.roles) and not miembro.bot
        ]

        if len(miembros) == 0:
            await interaction.response.send_message("No hay estudiantes conectados.")
            return

        for miembro in miembros:
            await miembro.iniciarContador()

        # Retorna formateado los nombres de Staff de tal forma: ["jsolis","apalacios","bgarcia","akelly"]
        staff = self.InputStaff.value.replace(' ','').split(',') if self.InputStaff.value != "" else []
        
        Office = Offices(ID, interaction.user.display_name[8:], miembros, Bloque, self.CanalDeVoz, staff)
        self.SIG.CanalesDeVoz[str(self.CanalDeVoz.id)] = ID
        self.SIG.OfficesLista[ID] = Office
        await Office.Barrido50()
        
        staffNombres = " "
        if self.InputStaff.value == "":
            staffNombres =  "No se registraron los codigos de staff!!!!"
        else:
            for Nombres in staff:
                staffNombres += Nombres + " "

        embed = CrearMensajeEmbed("Offices Inicializada :)", f"Datos: \n\tId -> {ID}\n\tBloque -> {Bloque}\n\tCodigos de Staff -> {staffNombres}")
        await interaction.response.send_message(embed=embed)