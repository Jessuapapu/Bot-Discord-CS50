from discord import Member
import asyncio
class Estudiante:
    def __init__(self, Usuario: Member | None, IdOffices):
        # Como los estudiantes estan formateados con primero grupo luego su nombre de ahi se obtiene su nombre
        self.IdUsuario = Usuario.display_name[10:]
        self.Usuario = Usuario
        self.IdDiscord = Usuario.id
        
        # Como los estudiantes estan formateados con primero grupo luego su nombre de ahi se obtiene su grupo
        self.grupo = Usuario.display_name[:7]
        self.IdOffice = IdOffices
        self.TiempoTotal = 0
        self.cumplimientoReal = 0
        
        # Validar contador y no se hagan 2 o mas
        self.Contador = None

    def calcularCumplimieto(self):
        # Valida si ha estado al menos 20 minutos en la offices
        if round(self.TiempoTotal/3600,1) >= 1.75:
            self.cumplimientoReal = 2.0
        
        elif round(self.TiempoTotal/3600,1) >= 1.3:
            self.cumplimientoReal = 1.5
        
        elif round(self.TiempoTotal/3600,1) >= 0.75:
            self.cumplimientoReal = 1
            
        elif round(self.TiempoTotal/3600,1) >= 0.3:
            self.cumplimientoReal = 0.5
                 
        else:
            self.cumplimientoReal = 0.0
        
        return
    
    async def DetenerContador(self):
        if self.Contador and not self.Contador.done():
            self.Contador.cancel()
            try:
                await self.Contador
            except asyncio.CancelledError:
                pass
        self.calcularCumplimieto()
    
    
    async def iniciarContador(self):
        # Si ya hay un contador activo, cancelarlo y luego volver activarlo
        if self.Contador is not None:
            if not self.Contador.done():
                self.Contador.cancel()
            try:
                await self.Contador
            except asyncio.CancelledError:
                pass

        # Crear uno nuevo y asignarlo
        self.Contador = asyncio.create_task(self.CalcularTiempo())

    
    async def CalcularTiempo(self):
        try:
            while True:
                await asyncio.sleep(1)
                self.TiempoTotal += 1
        except asyncio.CancelledError:
            pass
    
    def toString(self):
        return f"{self.IdUsuario} | {self.grupo} | {self.cumplimientoReal} \n"
    
    # Forma de comparar duplicados
    def __eq__(self, other):
        return (isinstance(other,Estudiante) and self.IdDiscord == other.IdDiscord)
    
    def __hash__(self):
        return hash(self.IdDiscord)

        
        