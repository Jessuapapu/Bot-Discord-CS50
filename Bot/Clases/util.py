import asyncio
class Offices:
    def __init__(self, Id, IdUsuario, TiempoInicio: float, TiempoFinal: float, Usuarios: list):
        self.Id = Id
        self.IdUsuario = IdUsuario
        self.TimepoInicio = TiempoInicio
        self.TiempoFinal = TiempoFinal
        self.Usuarios = Usuarios

class Estudiante:
    def __init__(self, IdUsuario, IdOffices):
        self.IdUsuario = IdUsuario
        self.IdOffice = IdOffices
        self.TiempoTotal = 0
    
    async def CalcularTiempo(self):
        try:
            while True:
                await asyncio.sleep(1)
                self.TiempoTotal += 1
        except asyncio.CancelledError:
            pass

    async def DetenerContador(self, Funcion):
        Funcion.cancel()
        

class fomratoEstudiante:
    def __init__(self,Nick,cumplimiento):
        self.grupo = Nick[:7]
        self.nombre = Nick[10:]
        self.cumplimiento = round(cumplimiento/3600,2)
    
    def toString(self):
        return f"{self.nombre} | {self.grupo} | {self.cumplimiento} \n"
        
        
def VerificacionRoles(Roles:list):
    RolesAceptados = ['Admin Discord','Staff']
    if Roles[len(Roles) - 1] not in RolesAceptados:
        return False
    return True
            
# Argumentos Aceptados para los comandos 
ArgumentosBuscar =  ["buscar","encontrar"]
ArgumentosObtener = ["obtener","descargar"]
ArgumentosListar = ["list","listar"]
ArgumentosEliminar = ["borrar","delete","eliminar","desaparecer"]
# Argumentos para iniciar offices
ArgumentosEmpezar = ["begin", "empezar", "comienzo", "1", "inicio", "carlosachambear", "chambeo"]
# Argumentos para finalizar Offices
ArgumentosTerminar = ["finalizar","terminar","0","finally","carlosterminachambear"]