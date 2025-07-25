from discord import Interaction, VoiceChannel, Member
from discord.ext import commands
from discord import app_commands


from Clases import util
from Clases.Decoradores import valida_id_office, valida_roles 
from CommandOffices import Empezar, Finalizar, Guardar, Votaciones, Ruleta, Editar, Listar, Mover, agregar
from CommandPdf import Obtener, Eliminar



class Offices(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Grupo Principal
    offices = app_commands.Group(name="offices", description="Comando para gestionar offices")


    # Subgrupo PDF
    pdf = app_commands.Group(name="pdf", description="Comandos para gestionar PDF")
    offices.add_command(pdf)
    
    
    # Subgrupo Editar
    editar = app_commands.Group(name="editar", description="Comandos para editar cositas")
    offices.add_command(editar)
    
    
    # Subgrupo Listar
    listar = app_commands.Group(name="listar", description="Comando para listar cositas")
    offices.add_command(listar)
    

    @offices.command(name="empezar", description="Inicia una office")
    @app_commands.describe(canalvoz="Nombre del canal de voz")
    @valida_roles()
    async def empezar(self, interaction: Interaction, canalvoz: VoiceChannel):
        await Empezar.empezar(interaction, canalvoz)



    @offices.command(name="terminar", description="Finaliza una office")
    @app_commands.describe(id="ID de la Office")
    @app_commands.autocomplete(id=util.officesActivasId_autocomplete)
    @valida_roles()
    @valida_id_office()
    async def terminar(self, interaction: Interaction, id: str):
        await Finalizar.finalizar(interaction, id)



    @offices.command(name="guardar", description="Guarda una office")
    @app_commands.describe(id="ID de la Office")
    @app_commands.autocomplete(id=util.officesRevisionId_autocomplete)
    @valida_roles()
    @valida_id_office()
    async def guardar(self, interaction: Interaction, id: str):
        await Guardar.guardar(interaction, id)
        
        
        
    @pdf.command(name="obtener", description="Obtiene un PDF de las offices")
    @app_commands.describe(nombre="Nombre del archivo PDF")
    @app_commands.autocomplete(nombre=util.Pdfs_autocomplete)
    @valida_roles()
    async def obtener_pdf(self, interaction: Interaction, nombre: str):
        await Obtener.obtener(interaction, nombre)



    @pdf.command(name="eliminar", description="Elimina un PDF de las offices")
    @app_commands.describe(nombre="Nombre del archivo PDF")
    @app_commands.autocomplete(nombre=util.Pdfs_autocomplete)
    @valida_roles()
    async def eliminar_pdf(self, interaction: Interaction, nombre: str):
        await Eliminar.eliminar(interaction, nombre)



    @offices.command(name="votacion", description="Realiza una votacion para los activos")
    @app_commands.describe(id="Id de offices activa",tiempo="el tiempo que esta activa la votacion")
    @app_commands.choices(tiempo=[
        app_commands.Choice(name='5 minutos', value=300.0),
        app_commands.Choice(name='10 minutos', value=600.0)
    ])
    @app_commands.autocomplete(id=util.officesActivasId_autocomplete)
    @valida_roles()
    @valida_id_office()
    async def votaciones(self,interation: Interaction, id:str, tiempo: app_commands.Choice[float]):
        await Votaciones.votacion(interation,id,tiempo.value)
        
    
    
    @offices.command(name="ruleta", description="Inicia una ruleta para la offices")
    @app_commands.describe(canalvoz="Nombre del canal de voz")
    @valida_roles()
    async def ruleta(self, interaction: Interaction, canalvoz: VoiceChannel):
        await Ruleta.ruletita(interaction,canalvoz)
        
    
    
    @editar.command(name="offices", description="Edita una office")
    @app_commands.describe(id="ID de la Office")
    @app_commands.autocomplete(id=util.officesTotal_autocomplete)
    @valida_roles()
    @valida_id_office()
    async def editarOffices(self, interaction: Interaction, id: str):
        await Editar.EditarOffices(interaction, id)
       
    
    
    @editar.command(name="estudiante", description="Edita a un estudiante")
    @app_commands.describe(id_offices="ID de la Office",estudiante="Nombra al estudiante")
    @app_commands.autocomplete(id_offices=util.officesTotal_autocomplete)
    @valida_roles()
    @valida_id_office()
    async def editar(self, interaction: Interaction, id_offices: str, estudiante: Member):
        await Editar.EditarEstudiante(interaction, id_offices, estudiante)
        
          
          
    @listar.command(name="estudiantes", description="Listar a los estudiantes de una offices")
    @app_commands.describe(id="ID de la Office")
    @app_commands.autocomplete(id=util.officesTotal_autocomplete)
    @valida_roles()
    @valida_id_office()
    async def listar_estudiantes(self, interaction: Interaction, id: str):
        await Listar.ListaEstudiantes(interaction, id)
    
    
    
    @listar.command(name="offices", description="Listar las offices activas o en revision")
    @valida_roles()
    async def listar_estudiantes(self, interaction: Interaction):
        await Listar.ListaOffices(interaction)
            
            
        
    @offices.command(name="mover", description="Mueve al autor del comando y a otro usuario a un canal de voz. sin que se pause su tiempo")
    @app_commands.describe(
        canal="Canal de voz al que serán movidos",
        miembro="Otro miembro que quieres mover"
    ) 
    async def mover(self,interaction: Interaction, canal: VoiceChannel, miembro: Member):
        await Mover.Mover(interaction,canal,miembro)
    
    
    @offices.command(name="agregar", description="Edita una office o a un estudiante")
    @app_commands.describe(id="ID de la Office", estudiante="Estudiante agregar")
    @app_commands.autocomplete(id=util.officesTotal_autocomplete)
    @valida_roles()
    @valida_id_office()
    async def agregar(self,interaction: Interaction, id: str, estudiante: Member):
        await agregar.agregarEstuOffices(interaction,id,estudiante)
                
                
                
async def setup(bot: commands.Bot):
    await bot.add_cog(Offices(bot))
