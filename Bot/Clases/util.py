
import os

from discord.app_commands import Choice
from discord import Interaction, Embed, ui, Color

from typing import List
from Declaraciones import Declaraciones
from table2ascii import table2ascii as t2a


Estado = Declaraciones.EstadoGlobal()

""" 

    Funciones Auxiliares 
    Funciones esenciales y son una forma de refactorizar el codigo, la mas inportante son los autocomplete

"""
# No necesario ya
# # Validacion de roles aceptados
# def VerificacionRoles(interaction):
#     RolesAceptados = ['Admin ','Staff']
#     # Se obtiene los roles de autor del mensaje
#     AutorRoles = [rol.name for rol in interaction.author.roles[1:]]

#     if AutorRoles[len(AutorRoles) - 1] not in RolesAceptados:
#         return False
#     return True

def CrearMensajeEmbed(Titulo = "", descripcion = "", color = Color.blue()) -> Embed:
    """ funcion encargada en crear mensajes embed """
    ListaEmbebida = Embed(  
            title=Titulo,     
            description = descripcion ,
            color=color
            )
    return ListaEmbebida
        
def CrearTabla(headers: list[str], Body: list[list[str]], Column_width: list[int] | None) -> str:
    """ Funcion encargada de crear una tabla"""
    # In your command:
    output = t2a(
        header = headers,
        body= Body,
        first_col_heading = True,
        column_widths = Column_width
    )
    return output



def CrearEncuestaSimple(Botones:list, tiempo) -> ui.View:
    """ Funcion encargada para generar Encuestas """
    view = ui.View(timeout = tiempo)
    
    for boton in Botones:
        view.add_item(boton.boton)
    
    return view



# Función de autocomplete
async def officesActivasId_autocomplete(interaction: Interaction, current: str) -> List[Choice[str]]:

    # Obtenemos todos los IDs de offices activas
    opciones = list(Estado.OfficesLista.keys())

    # Filtramos por lo que el usuario esté escribiendo (current)
    resultados = [
        Choice(name=office_id, value=office_id)
        for office_id in opciones if current.lower() in office_id.lower()
    ]

    return resultados[:25]  #  permite máximo 25 opciones por autocomplete

async def officesRevisionId_autocomplete(interaction: Interaction, current: str) -> List[Choice[str]]:

    # Obtenemos todos los IDs de offices activas
    opciones = list(Estado.OfficesRevision.keys())

    # Filtramos por lo que el usuario esté escribiendo (current)
    resultados = [
        Choice(name=office_id, value=office_id)
        for office_id in opciones if current.lower() in office_id.lower()
    ]

    return resultados[:25]  #  permite máximo 25 opciones por autocomplete


# Función de autocomplete
async def officesTotal_autocomplete(interaction: Interaction, current: str) -> List[Choice[str]]:

    # Obtenemos todos los IDs de offices activas
    opciones = list(Estado.OfficesLista.keys()) + list(Estado.OfficesRevision.keys()) 

    # Filtramos por lo que el usuario esté escribiendo (current)
    resultados = [
        Choice(name=office_id, value=office_id)
        for office_id in opciones if current.lower() in office_id.lower()
    ]

    return resultados[:25]  #  permite máximo 25 opciones por autocomplete


# Función de autocomplete
async def Pdfs_autocomplete(interaction: Interaction, current: str) -> List[Choice[str]]:

    # Obtenemos todos los IDs de offices activas
    ruta_Pdfs = "./Reportes"
    ListaArchivos = os.listdir(ruta_Pdfs)

    # Filtramos por lo que el usuario esté escribiendo (current)
    resultados = [
        Choice(name=Pdf, value=Pdf)
        for Pdf in ListaArchivos if current.lower() in Pdf.lower() and Pdf != 'si.txt'
    ]

    return resultados[:25]  #  permite máximo 25 opciones por autocomplete