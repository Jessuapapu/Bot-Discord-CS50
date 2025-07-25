from Clases.Formularios import FormularioBase
from Clases.util import CrearMensajeEmbed
from Declaraciones import Declaraciones
from discord import Interaction

Estado = Declaraciones.EstadoGlobal()

class formularioEditarOffices(FormularioBase.formularioBase):
    def __init__(self, title, IDOffices):
        super().__init__(title=title[:45])
        self.IDOffices = IDOffices
        self.Offices = Estado.getOffices(IDOffices)
        
        # # Tiene que entrar en uno
        # if self.IDOffices in Estado.getKeyOfficesLista():
        #     self.Offices = Estado.OfficesLista[self.IDOffices]
        # else:
        #     self.Offices = Estado.OfficesRevision[self.IDOffices]
            
        self.InputIdOffices = self.IniciarInput(f"Id: {self.IDOffices}", f"{self.IDOffices}", f"{self.IDOffices}",True)
        self.InputBloque = self.IniciarInput(f"Bloque de la offices : {self.Offices.bloque}", f"formato aceptado 10-12, 1-3, 3-5", f"{self.Offices.bloque}",True)
        
        nombres = " "
        if self.Offices.NombresStaff is not []:
            for nombress in self.Offices.NombresStaff:
                if nombress is not self.Offices.NombresStaff[len(self.Offices.NombresStaff) - 1 ]:
                    nombres += nombress + ", "
                else:
                    nombres += nombress
        else:
            nombres = ""               
                
        self.InputStaff = self.IniciarInput(f"Staff {nombres}","Ejem: pcastillo, dknauth, akelly, bgarcia",nombres, True)
        self.add_item(self.InputIdOffices)
        self.add_item(self.InputBloque) 
        self.add_item(self.InputStaff)
    
    
        
    async def on_submit(self, interaction: Interaction):
        
        if self.InputBloque == " " or not self.es_formato_valido(self.InputBloque.value, r"\b(\d{1,2})-(\d{1,2})\s*([aApP][mM])?\b"):
            await interaction.response.send_message("Error en el formato de las Horas",ephemeral=True)
            return
        
        
        if self.InputIdOffices.value in Estado.getKeyOfficesLista() + Estado.getKeyCanalesDeVoz() and not self.IDOffices:
            await interaction.response.send_message("Ya existe una offices con ese nombre",ephemeral=True)
        
        anteriorBloque = self.Offices.bloque
        anteriorId = self.Offices.Id
        anteriorstaff = self.Offices.NombresStaff
        
        
        try:
            del Estado.OfficesLista[self.IDOffices]
        except:
            del Estado.OfficesRevision[self.IDOffices]
            
            
        self.Offices.Id = self.InputIdOffices.value
        self.Offices.bloque = self.InputBloque.value
        self.Offices.NombresStaff = self.InputStaff.value.replace(' ','').split(',') if self.InputStaff.value != " " else []
        
        if self.Offices.Estado == 0:
            Estado.OfficesRevision[self.Offices.Id] = self.Offices
        elif self.Offices.Estado == 1:
            Estado.OfficesLista[self.Offices.Id] = self.Offices
        
        """ Encontrar diferencias entre los codigos de staffs
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

    