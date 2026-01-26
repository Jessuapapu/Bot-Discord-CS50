from Clases.Botones import BotonBase
from Clases import EstudianteClass
from Declaraciones import EstadoGlobal
Estado = EstadoGlobal.EstadoGlobal()
from discord import Interaction


class botonesEntrarOffices(BotonBase.botonBase):
    def __init__(self, label, style, IdOffices, Miembro):
        super().__init__(label, style)
        self.IdOffices = IdOffices
        self.miembro = Miembro  # string del ID de usuario
        self.boton.callback = self.callBack

    async def callBack(self, interaction: Interaction):
        
        if str(interaction.user.name) == str(self.miembro.name):
            
            NuevoEstu = EstudianteClass.Estudiante(self.miembro, self.IdOffices)
            Estado.OfficesLista[self.IdOffices].Usuarios.append(NuevoEstu)
            Estado.OfficesLista[self.IdOffices].ListaDeVotos[NuevoEstu.IdUsuario] = 0
            await NuevoEstu.iniciarContador()
            
            await interaction.response.send_message("``` Has sido añadido a la oficina correctamente.``` :clipboard: :writing_hand:")
        else:
            await interaction.response.send_message(" ``` No puedes usar este botón ya expiro o ya estas en la offices ```:eyes:", ephemeral=True)