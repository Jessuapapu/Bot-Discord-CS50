# Api de discord
import discord
from discord.ext import commands
# Modulos para las funciones del sistema y obtener el token de .env
import time
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

# Librerias para generar los PDFs -------------------------
#   Jinja La que genera el html a partir de una plantilla
from jinja2 import Environment, FileSystemLoader
#   xhtml2pdf genera el Pdf apartir del html generado con jinja (nota: NO sosporta bien el css y quedo mas o menos simple xd)
from xhtml2pdf import pisa

# Aun sin usar
import requests

# Definiciones de funciones y estructuras de datos
from Clases import util


# Permisos
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="$", intents=intents)

load_dotenv()  # Carga el .env
TOKEN = os.getenv("DISCORD_TOKEN")

# Estructuras globales
OfficesAGuardar = []
OfficesActivas = {}
CanalesDeVoz = []
ContadoresActivos = {}  # { str(user.id): (Estudiante, tarea, IdOffices) }



# ---------- COMANDO OFFICES ----------
# Comando Para iniciar o finalizar una Offices
@bot.command()
async def Offices(ctx, Estado: str, ID: str, CanalDeVoz: str):
    
    AutorRoles = [rol.name for rol in ctx.author.roles[1:]]

    # Validaciones
    if Estado.lower() not in util.ArgumentosEmpezar and Estado.lower() not in util.ArgumentosTerminar:
        await ctx.send("Error en el Argumento de Inicialización.")
        return
    
    CanalVoz = discord.utils.get(ctx.guild.voice_channels, name=CanalDeVoz)
    
    if not CanalVoz:
        await ctx.send("No se encontró el canal de voz.")
        return
    
    if len(CanalVoz.members) == 0:
        await ctx.send("No hay miembros conectados.")
        return
    
    if not util.VerificacionRoles(AutorRoles):
        await ctx.send("No tienes permisos.")
        return
    
    async def Empezar():
        # Empieza el proceso
        # valida si el usuario tiene un rol de admin o staff, si no es asi lo añade a la lista
        miembros = [
        util.Estudiante(str(miembro.display_name), ID) for miembro in CanalVoz.members
        if not any(rol.name in ["Staff", "Admin Discord"] for rol in miembro.roles)
        ]

        # Crea los contadores con su respectivo usuario
        for miembro in miembros:
            tarea = asyncio.create_task(miembro.CalcularTiempo())
            ContadoresActivos[miembro.IdUsuario] = (miembro, tarea)
            print(ContadoresActivos)

        Office = util.Offices(ID, ctx.author.id, time.time(), 0.0, miembros)
        CanalesDeVoz.append(CanalVoz.id)

        OfficesActivas[ID] = (Office)

        await ctx.send("Oficina iniciada correctamente.")
        return
    
    async def Finalizar():
        
        # Valida si hay offices activas
        if len(OfficesActivas) == 0:
            await ctx.send("No hay offices activas")
            return
        
        keys = []
        
        # Verifica si existe la offices
        try:
            Office = OfficesActivas[ID]
        except:
            await ctx.send("No se encontro esa offices")
            return
        Office.TiempoFinal = time.time()
               
        # Inteador en los contadores Activos para finalizar los contadores
        for contador in ContadoresActivos:
           Estudiante,tarea = ContadoresActivos[contador]
           # Se guardan las keys para borrarlos despues
           keys.append(Estudiante.IdUsuario)
           await ctx.send(f"Finalizando Offices {ID}")
           if Estudiante.IdOffice == ID:
               await ctx.send(f"Se esta guardando {Estudiante.IdUsuario} en la offices {ID}")
               await Estudiante.DetenerContador(tarea)
               
        OfficesActivas.pop(ID)
        OfficesAGuardar.append(Office)
        
        
        # Se Borran del diccionario que guarda los contadores activos
        for key in keys:
            Estudiante,tarea = ContadoresActivos[key]
            ContadoresActivos.pop(Estudiante.IdUsuario)
        
    # Valida si Es iniciar o finalizar    
    if Estado.lower() in util.ArgumentosEmpezar:
        asyncio.create_task(Empezar())
        return
    else:    
        asyncio.create_task(Finalizar())
        return


# Comando para Guardar las Offices Generadas en PDFs
@bot.command()
async def OfficesGuardar(ctx, ID):
    # Buscar la oficina por ID
    indiceOffices = 0
    SeEncontro = False
    
    for Content in OfficesAGuardar:
        
        if str(Content.Id) == str(ID):
            Contents = Content
            SeEncontro = True
            
            break
        indiceOffices += 1
        
    if not SeEncontro:
        await ctx.send("No se encontró la offices.")
        return

    # Formatear estudiantes
    Estudiantes = [
        util.fomratoEstudiante(user.IdUsuario, user.TiempoTotal)
        for user in Contents.Usuarios
    ]

    # Configurar entorno Jinja2
    ruta_plantillas = os.path.join(os.path.dirname(__file__), 'Plantilla')
    env = Environment(loader=FileSystemLoader(ruta_plantillas))
    template = env.get_template('Plantilla.html')

    # Renderizar HTML
    ahora = datetime.now()
    html_renderizado = template.render({
        "Estudiantes": Estudiantes,
        "Fecha": f"Día {ahora.day} del Mes {ahora.month}",
        "Offices": ID,
        "logo": os.path.join(ruta_plantillas, "Logo.png").replace("\\", "/")
    })

    # Generar PDF con xhtml2pdf
    ruta_pdf = os.path.join("./Reportes", f"Reporte {ID}.pdf")
    with open(ruta_pdf, "w+b") as resultado:
        pisa_status = pisa.CreatePDF(html_renderizado, dest=resultado)

    if pisa_status.err:
        await ctx.send("Error al generar el PDF.")
        return

    mensajeEmbebido = ""
    # Lista de Estudiantes formateada para el mensaje embebido
    for Estu in Estudiantes:
        mensajeEmbebido += Estu.toString()
        

    # Enviar mensaje y PDF
    #   Actualizacion el mesaje se cambio con una lista en un mesaje embebido
    ListaEmbebida = discord.Embed(
        
        description=mensajeEmbebido,
        color=discord.Color.blue()
    )
    
    # Se manda el mensaje embebido con su correspondiente archivo y se borra la offices de offices a guardar
    del OfficesAGuardar[indiceOffices]
    await ctx.send(embed=ListaEmbebida,file=discord.File(ruta_pdf))

@bot.command()
async def Obtenerpdf(ctx,Argumento,NombreDeArchivo = " "):
    ruta_Pdfs = "./Reportes"
    ListaArchivos = os.listdir(ruta_Pdfs)
    
    async def Listar():
        mensajeEmbebido = "Lista de Archivos\n"
        try:
            Pdf = [pdfs for pdfs in ListaArchivos]
            #   Genera el mensaje con la lista de pdfs
            for pdf in Pdf:
                mensajeEmbebido += f"{pdf}\n"
            ListaEmbebida = discord.Embed(       
            description=mensajeEmbebido,
            color=discord.Color.blue()
            )
            await ctx.send(embed = ListaEmbebida)
            return
        
        except:
            await ctx.send(f"Error al cargar los pdfs")
            return
        
    async def buscar():
        mensajeEmbebido = "Lista de Archivos\n"
        try:
            Pdf = [pdfs for pdfs in ListaArchivos if pdfs.startswith("Reporte " + NombreDeArchivo)]
            if Pdf == []:
                await ctx.send(f"No se encontro el archivo {NombreDeArchivo}")
                return 
            
            for pdf in Pdf:
                mensajeEmbebido += f"{pdf}\n"
            ListaEmbebida = discord.Embed(       
            description=mensajeEmbebido,
            color=discord.Color.green()
            )
            await ctx.send(embed = ListaEmbebida)
            return
        except:
            await ctx.send(f"Error Al buscar el pdf")
            return    

    async def obtener():
            Pdf = [pdfs for pdfs in ListaArchivos if pdfs.startswith("Reporte " + NombreDeArchivo)]
            
            for pdf in Pdf:
                if pdf == f"Reporte {NombreDeArchivo}.pdf":
                    await ctx.send(file=discord.File(ruta_Pdfs + f"/Reporte {NombreDeArchivo}.pdf"))
                    return

            await ctx.send(f"No se encontro el Id de archivo {NombreDeArchivo}")
            return 
    
    async def eliminar():
        Pdf = [pdfs for pdfs in ListaArchivos if pdfs.startswith("Reporte " + NombreDeArchivo)]
            
        for pdf in Pdf:
            if pdf == f"Reporte {NombreDeArchivo}.pdf":
                os.remove(ruta_Pdfs + f"/Reporte {NombreDeArchivo}.pdf")
                ListaEmbebida = discord.Embed(       
                description=f"Archivo Eliminado ",
                color=discord.Color.red()
                )
                await ctx.send(embed = ListaEmbebida)
                return
            
        await ctx.send(f"No se encontro el Id de archivo {NombreDeArchivo}")
        return 
    
    # Valida la entrada de argumentos       
    if Argumento.lower() in util.ArgumentosBuscar:
        asyncio.create_task(buscar())
    elif Argumento.lower() in util.ArgumentosListar:
        asyncio.create_task(Listar())
    elif Argumento.lower() in util.ArgumentosObtener:
        asyncio.create_task(obtener())
    elif Argumento.lower() in util.ArgumentosEliminar:
        asyncio.create_task(eliminar())
    else:
        await ctx.send("Error al obtener el Argumento")
        return
        
            
@bot.event
async def on_voice_state_update(member, before, after):
    user_id = str(member.display_name)
    
    # Si el usuario sale del canal de voz
    if before.channel and (after.channel is None or before.channel != after.channel):
        # Aqui se pausa (SE DETIENE) el contador
        """
        Primero se verifica si el canal al que entro en uno que esta activa una offices,
        luego se verifica si la persona esta en offices, si estas condiciones se cumlplen el contador se para
        """
        if before.channel.id in CanalesDeVoz and user_id in ContadoresActivos:
            estudiante, tarea = ContadoresActivos[user_id]
            await estudiante.DetenerContador(tarea)


    # Si el usuario entra o vuelve al canal de voz
    elif after.channel and after.channel.id in CanalesDeVoz:
        """
        Como en la funcion de salida primero se verifica si el canal esta con una Offices activa, luego se verifica si la persona esta en una offices, si es asi, si no tiene un contador activo (Esta en Pausa) lo activa
        """
        if user_id in ContadoresActivos:
            estudiante, _ = ContadoresActivos[user_id]
            nueva_tarea = asyncio.create_task(estudiante.CalcularTiempo())
            ContadoresActivos[user_id] = (estudiante, nueva_tarea)
            
bot.run(TOKEN)