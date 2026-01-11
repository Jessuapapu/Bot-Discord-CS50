from Clases.Formularios import FormularioBase
from Clases.util import CrearMensajeEmbed

from discord import Interaction


class formularioEditarOffices(FormularioBase.formularioBase):
    def __init__(self, title, IDOffices):
        super().__init__(title=title[:45], IdOffices= IDOffices)
            
        self.InputIdOffices = self.IniciarInput(f"Id: {self.IdOffices}", f"{self.IdOffices}", f"{self.IdOffices}",True)
        self.InputBloque.label = f"Bloque de la offices : {self.Offices.bloque}" 
        self.InputBloque.default = f"{self.Offices.bloque}"
        
        nombres = " "
        if self.Offices.NombresStaff is not []:
            for nombress in self.Offices.NombresStaff:
                if nombress is not self.Offices.NombresStaff[len(self.Offices.NombresStaff) - 1 ]:
                    nombres += nombress + ", "
                else:
                    nombres += nombress
        else:
            nombres = ""               
                
        self.InputStaff.label = f"Staff {nombres}"
        
        self.add_item(self.InputIdOffices)
        self.add_item(self.InputBloque) 
        self.add_item(self.InputStaff)
    
    
        
    async def on_submit(self, interaction: Interaction):
        
        if self.InputBloque == " " or not self.es_formato_valido(self.InputBloque.value, r"\b(\d{1,2})-(\d{1,2})\s*([aApP][mM])?\b"):
            await interaction.response.send_message("Error en el formato de las Horas",ephemeral=True)
            return
        
        
        if self.InputIdOffices.value in self.SIG.getKeyOfficesLista() + self.SIG.getKeyCanalesDeVoz() and not self.IDOffices:
            await interaction.response.send_message("Ya existe una offices con ese nombre",ephemeral=True)
        
        anteriorBloque = self.Offices.bloque
        anteriorId = self.Offices.Id
        anteriorstaff = self.Offices.NombresStaff
        
        
        try:
            del self.SIG.OfficesLista[self.IDOffices]
        except:
            del self.SIG.OfficesRevision[self.IDOffices]
            
            
        self.Offices.Id = self.InputIdOffices.value
        self.Offices.bloque = self.InputBloque.value
        self.Offices.NombresStaff = self.InputStaff.value.replace(' ','').split(',') if self.InputStaff.value != " " else []
        
        if self.Offices.Estado == 0:
            self.SIG.OfficesRevision[self.Offices.Id] = self.Offices
        elif self.Offices.Estado == 1:
            self.SIG.OfficesLista[self.Offices.Id] = self.Offices
        
        """  Encontrar diferencias entre los codigos de staffs
        psdt: A LO UNICO QUE LE PUSE ATENCION A MATEMATICAS DISCRETAS FUE A CONJUNTOS Y NO ME ARREPIENTO IKAUJSKAJSKAJSKJKSJAKSJSkjsKJSK
        
        la logica es simple, el problema nos da dos conjuntos, 
        La primera entrada de los codigos de staff (Los codigos de staff que se registraron cuando se inicio la offices)
        y La segunda entrada de los codigos de staff (Lo que se ingresaron al momento de editar)
        
        Para la primera entrada se le llamara A y a la segunda B
        
        Siendo que la Intersección de ambos conjuntos (A & B) son los codigos que no cambiaron, es decir lo codigos estan en ambos conjuntos
        y lo llamaremos Conjunto C
        
        Sabiendo esto, si hacemos una diferencia con respecto C a Ambos conjuntos (A y B) obtendremos los codigos que se eliminaron y se añadieron
        respectivamente 
        """

        ConjuntoA = set(anteriorstaff)
        ConjuntoB = set(self.Offices.NombresStaff)
        ConjuntoC = ConjuntoA & ConjuntoB
    
        Añadidos = ConjuntoB - ConjuntoC
        Eliminados = ConjuntoA - ConjuntoC
    
        # Construir mensaje condicionalmente
        staff_cambios = ""
        if not Añadidos and not Eliminados:
            staff_cambios = "Sin cambios en el staff."
        else:
            if Añadidos:
                staff_cambios += f"Staff añadido: {', '.join(Añadidos)}\n"
            if Eliminados:
                staff_cambios += f"Staff eliminado: {', '.join(Eliminados)}"
    
        # Crear embed
        embed = CrearMensajeEmbed(
            "Offices editada Correctamente :)",
            f"{anteriorId} -> {self.InputIdOffices.value}\n"
            f"{anteriorBloque} -> {self.InputBloque.value}\n"
            f"{staff_cambios}"
        )
        await interaction.response.send_message(embed=embed)

    