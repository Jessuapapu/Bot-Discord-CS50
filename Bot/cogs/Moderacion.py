from discord import Interaction, VoiceChannel, Member
from discord.ext import commands
from discord import app_commands

from Clases.Decoradores import valida_id_office, valida_roles, valida_roles_admin
from Clases import util
from Declaraciones import views, EstadoGlobal
from CommandModeracion import AutoModeracionFormatoEstu


class Administracion(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    administracion = app_commands.Group(
        name="administracion", description="Comandos para administracion del servidor")

    @valida_roles_admin()
    @administracion.command(
        name="crear_form_registro",
        description="comando que crea la auto asignacion del formato del estudiante"
    )
    async def crear_formulario_registro(self, interaction: Interaction):
        await AutoModeracionFormatoEstu.crear_boton_registro(interaction)

async def setup(bot: commands.Bot):
    await bot.add_cog(Administracion(bot))