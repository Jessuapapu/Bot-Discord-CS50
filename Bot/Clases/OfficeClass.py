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
        self.ListaDeVotos = self.generarListaDevotos() # IdUsuario: (cantidad de votos)
        self.ControlDeVotos = {}
        
        # Se refiere al estado, 1: Activa, 0: Finalizada
        self.Estado = 1
        
    def generarListaDevotos(self):
        ListaDeVotos = {}
        for user in self.Usuarios:
            ListaDeVotos[user.IdUsuario] = 0
            
        return ListaDeVotos
            
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
        
        try:
            while True:
                unique_names = []
                for user in self.Usuarios:
                    if user not in unique_names:
                        unique_names.append(user)

                self.Usuarios = unique_names
                await asyncio.sleep(900)
        except asyncio.CancelledError:
                pass