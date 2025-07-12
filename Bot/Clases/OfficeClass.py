import discord
import datetime, asyncio

class Offices:
    def __init__(self, Id, IdUsuario, Usuarios: list, bloque, CanalVoz: discord.VoiceChannel):
        hora = datetime.datetime.now()
        
        # Informacion de la offices
        self.Id = Id
        self.IdUsuario = IdUsuario
        self.HoraCreacion = hora.strftime("%H:%M")
        self.bloque = bloque
        self.canal = CanalVoz 
        
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
                
                tmp = set(self.Usuarios)
                for User in tmp:
                    await User.iniciarContador()
                self.Usuarios = list(tmp)

                await asyncio.sleep(30*60)
        except asyncio.CancelledError:
                pass