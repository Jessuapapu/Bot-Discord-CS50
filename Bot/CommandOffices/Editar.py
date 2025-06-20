import discord
import asyncio
from Declaraciones import Declaraciones
from Clases import util, SelectMenus

Estado = Declaraciones.EstadoGlobal()

async def Editar(interaction: discord.Interaction, IDOffices):
    headerTabla = ["Nombre", "Grupo", "Cumplimiento", "votos"]
    contenidoTabla = []

    Contents = Estado.OfficesRevision[IDOffices]
    for estu in Contents.Usuarios:
        contenidoTabla.append([
            estu.IdUsuario,
            estu.grupo,
            estu.cumplimientoReal,
            Contents.ListaDeVotos[estu.IdUsuario]
        ])

    tabla = util.CrearTabla(headerTabla, contenidoTabla)
    embed = util.CrearMensajeEmbed(
        "Estudiantes disponibles para editar",
        f"Selecciona uno del menú.\n```\n{tabla}\n```",
        discord.Color.dark_gold()
    )

    view = SelectMenus.SelectEstudianteView(Contents.Usuarios, IDOffices)
    await interaction.response.send_message(embed=embed, view=view)

