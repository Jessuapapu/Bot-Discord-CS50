from discord import VoiceChannel
from Clases.EstudianteClass import Estudiante
import datetime, asyncio

class Offices:
    """
    Clase Offices
    Representa una "office" o sesión de grupo en Discord, gestionando usuarios, staff, votos y limpieza periódica.
    
        Id (int): Identificador único de la office.
        IdUsuario (int): Identificador del usuario creador de la office.
        HoraCreacion (str): Hora en la que se creó la office (formato HH:MM).
        bloque (Any): Información adicional sobre el bloque o grupo al que pertenece la office.
        canal (VoiceChannel): Canal de voz de Discord asociado a la office.
        NombresStaff (list): Lista de nombres del staff asignado a la office.
        Usuarios (list): Lista de estudiantes activos en la office.
        ListaDeVotos (dict): Diccionario que almacena los votos de cada usuario.
        ControlDeVotos (dict): Diccionario para el control de votos durante la sesión.
        Estado (int): Estado actual de la office (1: Activa, 0: Finalizada).
        _Limpieza (asyncio.Task): Tarea asíncrona para la limpieza periódica de la lista de usuarios.
        
    Métodos:
        generarListaDevotos() -> dict:
            Genera y retorna un diccionario con los usuarios y la cantidad de votos inicializada en 0.
        getEstudiantes() -> list:
            Retorna una lista con los identificadores de usuario de los estudiantes activos.
        getNombreEstudiantes() -> list:
            Retorna una lista con los identificadores de usuario de los estudiantes activos (igual que getEstudiantes).
        getUnicoEstudiante(IdUsuario) -> Estudiante | None:
            Retorna el objeto usuario correspondiente al IdUsuario dado, o None si no existe.
        iniciarContadorDeVotos():
            Inicializa o reinicia el contador de votos para todos los estudiantes.
        async Barrido50():
            Inicia la tarea asíncrona de limpieza periódica de la lista de usuarios.
        async limpieza():
            Realiza la limpieza periódica de la lista de usuarios, eliminando duplicados y reiniciando contadores.
        setStaff(Nombres: list[str]):
            Asigna la lista de nombres del staff a la office.
   """
    def __init__(self, Id, IdUsuario, Usuarios: list[Estudiante], bloque, CanalVoz: VoiceChannel, Staff: list = []):
        hora = datetime.datetime.now()
        
        # Informacion de la offices
        self.Id = Id
        self.IdUsuario = IdUsuario
        self.HoraCreacion = hora.strftime("%H:%M")
        self.bloque = bloque
        self.canal = CanalVoz
        
        # Informacion del Staff
        self.NombresStaff = Staff
        
        # Es la lista de estudiantes activos
        self.Usuarios = Usuarios
        self.ListaDeVotos = self.generarListaDevotos() 
        self.ControlDeVotos = {}
        
        # Se refiere al estado, 1: Activa, 0: Finalizada
        self.Estado = 1
        
        self._Limpieza = None
        
        
        
    def generarListaDevotos(self) -> dict:
        """ 
        Generla Lista de Votos total para la offices, esto es actuamatizado al principio de la offices de forma de constructor
        
            retorna ->  IdUsuario: (cantidad de votos) 
        """
        ListaDeVotos = {}
        for user in self.Usuarios:
            try:
                if ListaDeVotos[user.IdUsuario] > 0:
                    ListaDeVotos[user.IdUsuario] = ListaDeVotos[user.IdUsuario]
            except:
                ListaDeVotos[user.IdUsuario] = 0
            
        return ListaDeVotos
     
     # Creo que se puede refactorizar mejor esto       
    def getEstudiantes(self):
        return [user.IdUsuario for user in self.Usuarios]
    
    def getNombreEstudiantes(self):
        return [user.IdUsuario for user in self.Usuarios]
    
    def getUnicoEstudiante(self,IdUsuario):
        # si no lo encuentra retorna None
        for user in self.Usuarios:
            if IdUsuario == user.IdUsuario:
                return user
       
        return None   
    
    def iniciarContadorDeVotos(self):
        if len(list(self.ControlDeVotos.keys())) == 0:
            for nombre in self.getNombreEstudiantes():
                self.ControlDeVotos[nombre] = 0
            return
        
        else:
            for nombre in list(self.ControlDeVotos.keys()):
                del self.ControlDeVotos[nombre]
            self.iniciarContadorDeVotos()
    
    async def Barrido50(self):  
        if self._Limpieza is not None:
            if not self._Limpieza.done():
                self._Limpieza.cancel()
        
        self._Limpieza = asyncio.create_task(self.limpieza())
            
            
    async def limpieza(self):
        try:
            while True:
                if self.Estado != 1:
                    break
                
                # Eliminar duplicados manteniendo el orden
                tmp = list(dict.fromkeys(self.Usuarios))

                for User in tmp:
                    await User.iniciarContador()

                self.Usuarios = tmp

                await asyncio.sleep(30*60)
        except asyncio.CancelledError:
            pass

            
            
    def setStaff(self,Nombres:list[str]):
        self.NombresStaff = Nombres
        return