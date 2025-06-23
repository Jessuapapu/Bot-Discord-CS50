import asyncio
import discord
import os

from discord import app_commands
from typing import List
from Declaraciones import Declaraciones
from table2ascii import table2ascii as t2a
import datetime

Estado = Declaraciones.EstadoGlobal()


class Offices:
    def __init__(self, Id, IdUsuario, Usuarios: list,bloque):
        hora = datetime.datetime.now()
        
        # Informacion de la offices
        self.Id = Id
        self.IdUsuario = IdUsuario
        self.HoraCreacion = hora.strftime("%H:%M")
        self.bloque = bloque
        
        # Es la lista de estudiantes activos
        self.Usuarios = Usuarios
        self.ListaDeVotos = self.generarListaDevotos() # IdUsuario: (cantidad de votos)
        
        
        # Se refiere al estado, 1: Activa, 0: Finalizada, 2: revision
        self.Estado = 1
        
    def generarListaDevotos(self):
        ListaDeVotos = {}
        for user in self.Usuarios:
            ListaDeVotos[user.IdUsuario] = 0
        return ListaDeVotos
            
    def getEstudiantes(self):
        return [user.IdUsuario for user in self.Usuarios]
            
        

class Estudiante:
    def __init__(self, Usuario, IdOffices):
        # Como los estudiantes estan formateados con primero grupo luego su nombre de ahi se obtiene su nombre
        self.IdUsuario = Usuario.display_name[10:]
        self.Usuario = Usuario
        # Como los estudiantes estan formateados con primero grupo luego su nombre de ahi se obtiene su grupo
        self.grupo = Usuario.display_name[:7]
        self.IdOffice = IdOffices
        self.TiempoTotal = 0
        self.cumplimientoReal = 0

    def calcularCumplimieto(self):
        # Valida si ha estado al menos 30 minutos en la offices
        if round(self.TiempoTotal/3600,1) > 0.25:
            self.cumplimientoReal = round(self.TiempoTotal/3600,1)
        else:
            self.cumplimientoReal = 0.0
        
        return
    
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
    
    def toString(self):
        return f"{self.IdUsuario} | {self.grupo} | {self.cumplimientoReal} \n"
        

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
def CrearMensajeEmbed(Titulo = "", descripcion = "", color = discord.Color.blue()):
    ListaEmbebida = discord.Embed(  
            title=Titulo,     
            description = descripcion ,
            color=color
            )
    return ListaEmbebida
        
def CrearTabla(headers: list, Body: list):
    # In your command:
    output = t2a(
        header=headers,
        body= Body,
        first_col_heading=True
    )
    return output


# Función de autocomplete
async def officesActivasId_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:

    # Obtenemos todos los IDs de offices activas
    opciones = list(Estado.OfficesLista.keys())

    # Filtramos por lo que el usuario esté escribiendo (current)
    resultados = [
        app_commands.Choice(name=office_id, value=office_id)
        for office_id in opciones if current.lower() in office_id.lower()
    ]

    return resultados[:25]  # Discord permite máximo 25 opciones por autocomplete

async def officesRevisionId_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:

    # Obtenemos todos los IDs de offices activas
    opciones = list(Estado.OfficesRevision.keys())

    # Filtramos por lo que el usuario esté escribiendo (current)
    resultados = [
        app_commands.Choice(name=office_id, value=office_id)
        for office_id in opciones if current.lower() in office_id.lower()
    ]

    return resultados[:25]  # Discord permite máximo 25 opciones por autocomplete


# Función de autocomplete
async def officesTotal_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:

    # Obtenemos todos los IDs de offices activas
    opciones = list(Estado.OfficesLista.keys()) + list(Estado.OfficesRevision.keys()) 

    # Filtramos por lo que el usuario esté escribiendo (current)
    resultados = [
        app_commands.Choice(name=office_id, value=office_id)
        for office_id in opciones if current.lower() in office_id.lower()
    ]

    return resultados[:25]  # Discord permite máximo 25 opciones por autocomplete


# Función de autocomplete
async def Pdfs_autocomplete(interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:

    # Obtenemos todos los IDs de offices activas
    ruta_Pdfs = "./Reportes"
    ListaArchivos = os.listdir(ruta_Pdfs)

    # Filtramos por lo que el usuario esté escribiendo (current)
    resultados = [
        app_commands.Choice(name=Pdf, value=Pdf)
        for Pdf in ListaArchivos if current.lower() in Pdf.lower()
    ]

    return resultados[:25]  # Discord permite máximo 25 opciones por autocomplete


# Generar Encuestas
def CrearEncuestaSimple( Botones:list, tiempo):
    view = discord.ui.View(timeout = tiempo)
    
    for boton in Botones:
        view.add_item(boton.boton)
    
    return view
