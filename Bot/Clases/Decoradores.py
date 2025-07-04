import functools
import discord
from Declaraciones import Declaraciones

Estado = Declaraciones.EstadoGlobal()
import functools
from Declaraciones import Declaraciones

Estado = Declaraciones.EstadoGlobal()

def valida_id_office():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, interaction, *args, **kwargs):
            id_office = kwargs.pop("id", None)  # Elimina 'id' de kwargs si está

            if id_office is None and args:
                id_office = args[0]
                args = args[1:]  # Remueve 'id' de args

            if id_office not in Estado.getKeyOfficesLista() + Estado.getKeyOfficesRevision():
                await interaction.response.send_message("❌ La office indicada no existe.", ephemeral=True)
                return

            # Llama a la función con el 'id' solo una vez
            return await func(self, interaction, id_office, *args, **kwargs)

        return wrapper
    return decorator


def valida_roles():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, interaction: discord.Interaction, *args, **kwargs):
            # Obtenemos todos los nombres de roles del usuario
            AutorRoles = [rol.name for rol in interaction.user.roles]

            # Validamos si tiene alguno de los roles permitidos
            if not any(rol in ["Staff", "Admin Staff"] for rol in AutorRoles):
                await interaction.response.send_message(
                    "❌ No tienes los permisos requeridos.",
                    ephemeral=True
                )
                return

            # Llamamos a la función original
            return await func(self, interaction, *args, **kwargs)
        return wrapper
    return decorator
