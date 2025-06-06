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
                # Aquí podrías hacer un print para depurar si deseas
        except asyncio.CancelledError:
            pass

    async def DetenerContador(self, Funcion):
        Funcion.cancel()
        print(f"Tiempo total acumulado: {self.TiempoTotal} segundos")

def VerificacionRoles(Roles:list):
    RolesAceptados = ['Admin Discord','Staff']
    if Roles[len(Roles) - 1] not in RolesAceptados:
        return False
    return True

class fomratoEstudiante:
    def __init__(self,Nick,cumplimiento):
        self.grupo = Nick[:7]
        self.nombre = Nick[10:]
        self.cumplimiento = cumplimiento
        
        

            

ArgumentosAceptados = ["begin", "empezar", "comienzo", "1", "inicio", "carlosachambear", "chambeo", "finalizar","terminar","0","finally","carlosterminachambear"]
ArgumentosEmpezar = ArgumentosAceptados[:7]
ArgumentosTerminar = ArgumentosAceptados[7:]