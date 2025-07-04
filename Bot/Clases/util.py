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
        
        # Validar contador y no se hagan 2 o mas
        self.Contador = None

    def calcularCumplimieto(self):
        # Valida si ha estado al menos 30 minutos en la offices
        if round(self.TiempoTotal/3600,1) >= 1.9:
            self.cumplimientoReal = 2.0
        
        elif round(self.TiempoTotal/3600,1) >= 1.3:
            self.cumplimientoReal = 1.5
        
        elif round(self.TiempoTotal/3600,1) >= 1:
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
        # Si ya hay un contador activo, cancelarlo y esperarlo
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
        for Pdf in ListaArchivos if current.lower() in Pdf.lower() and Pdf != 'si.txt'
    ]

    return resultados[:25]  # Discord permite máximo 25 opciones por autocomplete


# Generar Encuestas
def CrearEncuestaSimple( Botones:list, tiempo):
    view = discord.ui.View(timeout = tiempo)
    
    for boton in Botones:
        view.add_item(boton.boton)
    
    return view
