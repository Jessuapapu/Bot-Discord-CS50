from Clases.Formularios import FormularioBase


class FormularioFormato(FormularioBase.formularioBase):
    
    def __init__(self, title):
        super().__init__(title)
        self.inputNombre = self.IniciarInput("Ingresa tu Nombre","", None, True)
        self.inputCodigo = self.IniciarInput("Ingresa tu codigo de docs","", None, True)
        
        self.add_item(self.inputCodigo)
        self.add_item(self.inputNombre)
        
    # TODO: Esto va conectado a la base de datos
    async def on_submit(self):
        pass
        
    