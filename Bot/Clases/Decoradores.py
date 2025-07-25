import functools
from discord import Interaction
from Declaraciones import Declaraciones

Estado = Declaraciones.EstadoGlobal()


def valida_id_office():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, interaction, *args, **kwargs):
            id_office = None

            # 1. Buscar en kwargs
            if "id_offices" in kwargs:
                id_office = kwargs.pop("id_offices")
            elif "id" in kwargs:
                id_office = kwargs.pop("id")
            
            # 2. Si aún no lo encuentra, buscar en args
            if id_office is None and args:
                id_office = args[0]
                args = args[1:]

            #  DEBUG: Verificar qué se está recibiendo
            # print(f"ID OFFICE RECIBIDO: {id_office}")
            # print("Oficinas válidas:", Estado.getKeyOfficesLista() + Estado.getKeyOfficesRevision())

            # 3. Validar
            if id_office not in Estado.getKeyOfficesLista() + Estado.getKeyOfficesRevision():
                await interaction.response.send_message("❌ La office indicada no existe.", ephemeral=True)
                return

            # 4. Ejecutar función decorada
            return await func(self, interaction, id_office, *args, **kwargs)

        return wrapper
    return decorator




def valida_roles():
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self, interaction: Interaction, *args, **kwargs):
            # Obtenemos todos los nombres de roles del usuario
            AutorRoles = [rol.name for rol in interaction.user.roles]

            # Validamos si tiene alguno de los roles permitidos
            if not any(rol in Estado.ListaDeRolesPermitidos for rol in AutorRoles):
                await interaction.response.send_message(
                    "❌ No tienes los permisos requeridos.",
                    ephemeral=True
                )
                return

            # Llamamos a la función original
            return await func(self, interaction, *args, **kwargs)
        return wrapper
    return decorator
