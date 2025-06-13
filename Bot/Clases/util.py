import asyncio
import discord

from discord import app_commands
from typing import List
from Declaraciones import Declaraciones

Estado = Declaraciones.EstadoGlobal()

class Offices:
    def __init__(self, Id, IdUsuario, Usuarios: list):
        
        # Id se refiere a su numero de offices
        self.Id = Id
        
        # Es el que creo la offices
        self.IdUsuario = IdUsuario
        
        # Es la lista de estudiantes activos
        self.Usuarios = Usuarios
        
        # Se refiere al estado 1: Activa, 0: Finalizada
        self.Estado = 1

class Estudiante:
    def __init__(self, IdUsuario, IdOffices):
        # Como los estudiantes estan formateados con primero grupo luego su nombre de ahi se obtiene su nombre
        self.IdUsuario = IdUsuario[10:]
        
        # Como los estudiantes estan formateados con primero grupo luego su nombre de ahi se obtiene su grupo
        self.grupo = IdUsuario[:7]
        self.IdOffice = IdOffices
        self.TiempoTotal = 0
        self.cumplimientoReal = 0

    def calcularCumplimieto(self):
        self.cumplimientoReal = round(self.TiempoTotal/3600,1)
        return
    
    def toString(self):
        return f"{self.IdUsuario} | {self.grupo} | {self.cumplimientoReal} \n"
    
    async def DetenerContador(self, Funcion):
        Funcion.cancel()
        self.calcularCumplimieto()
    
    async def CalcularTiempo(self):
        try:
            while True:
                await asyncio.sleep(1)
                self.TiempoTotal += 1
        except asyncio.CancelledError:
            pass
        
    
# Funciones Auxiliares
# Validacion de roles aceptados
def VerificacionRoles(interaction):
    RolesAceptados = ['Admin Discord','Staff']
    # Se obtiene los roles de autor del mensaje
    AutorRoles = [rol.name for rol in interaction.author.roles[1:]]

    if AutorRoles[len(AutorRoles) - 1] not in RolesAceptados:
        return False
    return True

# Crear mensajes embed
def CrearMensajeEmbed(Titulo = "",descripcion = "", color = discord.Color.blue()):
    ListaEmbebida = discord.Embed(  
            title=Titulo,     
            description = descripcion ,
            color=color
            )
    return ListaEmbebida
        
from typing import List


# Función de autocomplete
async def officesId_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:

    # Obtenemos todos los IDs de offices activas
    opciones = list(Estado.OfficesLista.keys())

    # Filtramos por lo que el usuario esté escribiendo (current)
    resultados = [
        app_commands.Choice(name=office_id, value=office_id)
        for office_id in opciones if current.lower() in office_id.lower()
    ]

    return resultados[:25]  # Discord permite máximo 25 opciones por autocomplete