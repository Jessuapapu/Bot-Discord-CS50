import discord
from Clases import EstudianteClass
from Declaraciones import Declaraciones
Estado = Declaraciones.EstadoGlobal()

class formularioEditarEstu(discord.ui.Modal):

    def __init__(self, title : str, IDOffices : str, Estudiante: EstudianteClass.Estudiante | discord.Member | str):
        super().__init__(title=title, timeout=5*60)
        self.IDOffices = IDOffices
        self.Estudiante = Estado.getEstudiante(Estudiante, IDOffices) if type(Estudiante) is not EstudianteClass.Estudiante else Estudiante
        self.Offices = Estado.getOffices(IDOffices)
        
        # # Tiene que entrar en uno (Refactorizado)
        # if self.IDOffices in Estado.getKeyOfficesLista():
        #     self.Offices = Estado.OfficesLista[self.IDOffices]
        # else:
        #     self.Offices = Estado.OfficesRevision[self.IDOffices]
        
        print()
        self.InputNombreEstudiante = self.IniciarInput("Nombre del estudiante", f"{self.Estudiante.IdUsuario}", self.Estudiante.IdUsuario)
        self.InputGrupoEstudiante = self.IniciarInput("Grupo del estudiante (Solo la letra)", f"{self.Estudiante.grupo[6]}", self.Estudiante.grupo[6])
        self.InputCumplimiento = self.IniciarInput(f"Cumplimiento {self.Estudiante.cumplimientoReal}","Rango aceptado: 0.0 - 2.0",f"{self.Estudiante.cumplimientoReal}")
        
        self.add_item(self.InputNombreEstudiante)
        self.add_item(self.InputGrupoEstudiante)
        self.add_item(self.InputCumplimiento)
    
    def IniciarInput(self, label = " ", placeholder = " ", default = " "):
        Input = discord.ui.TextInput(
            label= label,
            placeholder= placeholder, 
            default= default,
        )
        return Input
    
    
    async def on_submit(self, interaction):
        
        anteriorNombre = self.Estudiante.IdUsuario
        anteriorHora = self.Estudiante.cumplimientoReal
        anteriorGrupo = self.Estudiante.grupo
        
        if self.InputCumplimiento.value not in ["0.0","0.5","1.0","1.5","2.0"]:
            await interaction.response.send_message("Ingrese una hora valida (0.0, 0.5, 1.0, 1.5, 2.0)",ephemeral=True)
            return
        
        if self.InputGrupoEstudiante.value is None or self.InputGrupoEstudiante.value.lower() not in ["a","b","c","d","e","f","g","h","i"]:
            await interaction.response.send_message("Ingrese solo la letra del grupo A, B, C, D, E, F, G, H, I",ephemeral=True)
            return
        
        try:
            Inputnumero = float(self.InputCumplimiento.value)    
        except:
            await interaction.response.send_message("Error al tratar de obtener los datos nuevos, formato equivocado", ephemeral=True)
            return
        
        
        if Inputnumero > 2.0:
            await interaction.response.send_message("Sobre exceden el tiempo permitido", ephemeral=True)
            return
        
        self.Estudiante.IdUsuario = self.InputNombreEstudiante.value
        self.Estudiante.grupo = f"Grupo {self.InputGrupoEstudiante.value.upper()}"
        self.Estudiante.cumplimientoReal = Inputnumero
        self.Estudiante.TiempoTotal = Inputnumero * 3600 if Inputnumero > 0.0 else 0
        
        if self.Offices.Estado == 0:
            for i,user in enumerate(Estado.OfficesRevision[self.Offices.Id].Usuarios):
                if user == anteriorNombre:
                    Estado.OfficesRevision[self.Offices.Id].Usuarios[i] = self.Estudiante
                    
        elif self.Offices.Estado == 1:
            for i,user in enumerate(Estado.OfficesLista[self.Offices.Id].Usuarios):
                if user == anteriorNombre:
                    Estado.OfficesLista[self.Offices.Id].Usuarios[i] = self.Estudiante
        
        await interaction.response.send_message(f"Datos del estudiante han sido cambiado Correctamente, {anteriorNombre} -> {self.Estudiante.IdUsuario}, {anteriorHora} -> {Inputnumero}, {anteriorGrupo} -> Grupo {self.InputGrupoEstudiante} correctamente :)", ephemeral=True)
   

class formularioEditarOffices(discord.ui.Modal):
    def __init__(self, title, IDOffices):
        super().__init__(title=title[:45], timeout=5*60)
        self.IDOffices = IDOffices
        self.Offices = Estado.getOffices(IDOffices)
        
        # # Tiene que entrar en uno
        # if self.IDOffices in Estado.getKeyOfficesLista():
        #     self.Offices = Estado.OfficesLista[self.IDOffices]
        # else:
        #     self.Offices = Estado.OfficesRevision[self.IDOffices]
            
        self.InputIdOffices = self.IniciarInput(f"Offices: {self.IDOffices}", f"{self.IDOffices}", f"{self.IDOffices}")
        self.InputBloque = self.IniciarInput(f"Bloque de la offices : {self.Offices.bloque}", f"formato aceptado 10-12, 1-3, 3-5", f"{self.Offices.bloque}")
        
        self.add_item(self.InputIdOffices)
        self.add_item(self.InputBloque) 
        
    def IniciarInput(self, label = " ", placeholder = " ", default = " "):
        Input = discord.ui.TextInput(
            label= label,
            placeholder= placeholder, 
            default= default,
        )
        return Input
    
    async def on_submit(self, interaction):
        
        if self.InputBloque.value not in ["10-12","1-3","3-5","10 - 12","1 - 3","3 - 5"]:
            await interaction.response.send_message("Error en el formato de las Horas",ephemeral=True)
            return
        
        
        if self.InputIdOffices.value in Estado.getKeyOfficesLista() + Estado.getKeyCanalesDeVoz() and not self.IDOffices:
            await interaction.response.send_message("Ya existe una offices con ese nombre",ephemeral=True)
        
        anteriorBloque = self.Offices.bloque
        anteriorId = self.Offices.Id
        
        try:
            del Estado.OfficesLista[self.IDOffices]
        except:
            del Estado.OfficesRevision[self.IDOffices]
            
            
        self.Offices.Id = self.InputIdOffices.value
        self.Offices.bloque = self.InputBloque.value
        
        if self.Offices.Estado == 0:
            Estado.OfficesRevision[self.Offices.Id] = self.Offices
        elif self.Offices.Estado == 1:
            Estado.OfficesLista[self.Offices.Id] = self.Offices
        
        await interaction.response.send_message(f"Offices editada Correctamente :) {anteriorId} -> {self.InputIdOffices.value}, {anteriorBloque} -> {self.InputBloque.value}")
    
    
class formularioAgregarEstudiante(discord.ui.Modal):
    def __init__(self, title, IDOffices, DiscordMiembro : discord.Member):
        super().__init__(title=title, timeout=5*60)
        self.IDOffices = IDOffices
        self.Offices = Estado.getOffices(IDOffices)
        self.DiscordMiembro = DiscordMiembro # Se trata como si fuera un estudiante, pero es solo para obtener el miembro directo del servidor
        
        # Tiene que entrar en uno
        # try:
        #     self.Offices = Estado.OfficesLista[self.IDOffices]
        # except:
        #     self.Offices = Estado.OfficesRevision[self.IDOffices]
            
        #self.InputNombreEstudiante = self.IniciarInput("Nombre del estudiante", f"", None)
        #self.InputGrupoEstudiante = self.IniciarInput("Grupo del estudiante (Solo la letra)", f"", None)
        self.InputCumplimientoEstu = self.IniciarInput("Cumplimiento en Horas","Si esta activa se calcula el tiempo",0.0)

        #self.add_item(self.InputNombreEstudiante)
        #self.add_item(self.InputGrupoEstudiante)
        self.add_item(self.InputCumplimientoEstu)

        
    def IniciarInput(self, label = " ", placeholder = " ", default = " "):
        Input = discord.ui.TextInput(
            label = label,
            placeholder = placeholder, 
            default = default,
        )
        return Input
    
    async def on_submit(self, interaction):
        
        if self.InputCumplimientoEstu.value not in ["0.0","0.5","1.0","1.5","2.0"] or self.InputCumplimientoEstu.value is None:
            await interaction.response.send_message("Ingrese una hora valida (0.0, 0.5, 1.0, 1.5, 2.0)",ephemeral=True)
            return
        
        # Innecesario, pero de una forma de colocar el nombre
        """if self.InputNombreEstudiante is None:
            await interaction.response.send_message("Ingrese un Nombre Valido",ephemeral=True)
            return"""
        
        # Innecesario, pero es otra forma de colocar el grupo
        """if self.InputGrupoEstudiante.value.lower() not in ["a","b","c","d","e","f","g","h","i"] or self.InputGrupoEstudiante is None:
            await interaction.response.send_message("Ingrese solo la letra del grupo A, B, C, D, E, F, G, H, I",ephemeral=True)
            return"""
        
            
        EstudianteNuevo = EstudianteClass.Estudiante(self.DiscordMiembro,self.IDOffices)
        EstudianteNuevo.cumplimientoReal = float(self.InputCumplimientoEstu.value)
        
        
        if self.Offices.Estado == 0:
            if self.validarDuplicados(EstudianteNuevo,Estado.OfficesRevision[self.Offices.Id].Usuarios):
                Estado.OfficesRevision[self.Offices.Id].Usuarios.append(EstudianteNuevo)
                Estado.OfficesRevision[self.Offices.Id].ListaDeVotos[EstudianteNuevo.IdUsuario] = 0
            else:
                await interaction.response.send_message("Estudiante Duplicado :(")
                return 
            
        elif self.Offices.Estado == 1:
            if  self.validarDuplicados(EstudianteNuevo,Estado.OfficesLista[self.Offices.Id].Usuarios):
                EstudianteNuevo.TiempoTotal = round(float(self.InputCumplimientoEstu.value) * 3600)
                await EstudianteNuevo.iniciarContador()
                Estado.OfficesLista[self.Offices.Id].Usuarios.append(EstudianteNuevo)
                Estado.OfficesLista[self.Offices.Id].ListaDeVotos[EstudianteNuevo.IdUsuario] = 0
            else:
                await interaction.response.send_message("Estudiante Duplicado :(")
                return
                
        
        await interaction.response.send_message("Estudiante agregado Correctamente :)")
        
        
    def validarDuplicados(self,Estu:EstudianteClass.Estudiante,lista):
        for User in lista:
            if Estu.IdDiscord == User.IdDiscord:
                return False
        
        return True
        