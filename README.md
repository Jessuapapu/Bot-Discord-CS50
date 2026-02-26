
# 🤖 Bot Discord CS50

Este repositorio contiene el código fuente de un bot de Discord diseñado para facilitar
la gestión de *offices* (sesiones de ayuda) y estudiantes en el contexto del curso **CS50**.
El bot hace un amplio uso de las APIs modernas de Discord (`discord.py v2.x`), incluyendo
**slash commands**, **modals**, **select menus** y **componentes interactivos** para
ofrecer una experiencia fluida y validada tanto para usuarios finales como para el personal
administrativo.

---

## 📌 Descripción general

El objetivo principal del bot es centralizar las actividades alrededor de los offices:
- Controlar entradas y salidas de estudiantes en canales de voz.
- Llevar registro de tiempos y asistencia.
- Proveer herramientas de edición, listado y traslado sin interrumpir el cronómetro.

Además, el bot incluye un módulo de **moderación/seguridad** con funcionalidades de
anti‑spam, detección de links maliciosos y comandos administrativos para desplegar formularios
de registro automatizados.

Un servicio externo (configurable mediante variables de entorno) alimenta la caché de
ofices y estudiantes, permitiendo que el bot trabaje con una copia local rápidamente
sin depender constantemente de la API externa.


## 🚀 Características destacadas

- **Gestión de offices**: iniciar, terminar, guardar, editar, listar, votar, ruleta, mover
y agregar estudiantes.
- **Comandos organizados** en grupos `/offices` con subgrupos `/pdf`, `/editar` y `/listar`.
- **Formularios (`Modals`) y select menus** para añadir/editar oficinas y estudiantes con
  validación de datos integrada.
- **Votaciones** temporizadas y **ruletas** para seleccionar canales de voz.
- **Seguridad**: anti‑spam, bloqueo de enlaces maliciosos y seguimiento de estados de voz.
- **Administración**: creación de mensajes persistentes con botones para el registro
automático de estudiantes.
- **Integración con servicio web** para sincronizar oficinas y estudiantes.
- **Generación, descarga y eliminación de PDFs** relacionados a las oficinas.

---

## 🛠 Instalación & configuración

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/Jessuapapu/Bot-Discord-CS50.git
   cd Bot-Discord-CS50
   ```

2. **Crear un entorno virtual** (recomendado):

   ```powershell
   python -m venv env
   .\env\Scripts\Activate.ps1   # PowerShell
   # o env\Scripts\activate.bat    # cmd
   ```

3. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno** (archivo `.env` en la raíz):

   ```ini
   DISCORD_TOKEN=tu_token_del_bot
   LINK_SERVER=https://url-de-tu-servicio
   API_SERVER=tu_api_key
   DISCORD_ID_SERVER=ID_del_servidor_discord
   ```

   - `DISCORD_TOKEN`: token del bot obtenido desde el portal de desarrolladores de Discord.
   - `LINK_SERVER` & `API_SERVER`: dirección y clave de la API que administra oficinas.
   - `DISCORD_ID_SERVER`: ID numérico del servidor (guild) donde opera el bot.

5. **Ejecutar**:

   ```bash
   python Bot\main.py
   ```

   El bot registrará los *cogs* definidos en `Bot/cogs/` y se conectará al servidor.

---

## 🗂 Estructura del proyecto

```
Bot-Discord-CS50/
├─ Bot/
│  ├─ main.py             # Entrada principal
│  ├─ Clases/             # Clases auxiliares y utilidades
│  │  ├─ BotClass.py      # Subclase de discord.Bot con carga automática de cogs
│  │  ├─ Decoradores.py   # Validaciones de roles e IDs
│  │  ├─ EstudianteClass.py
│  │  ├─ OfficeClass.py
│  │  ├─ logs.py          # Manejador simple de logs
│  │  ├─ SelectMenus.py
│  │  ├─ util.py          # Helpers globales y autocompletados
│  │  ├─ Botones/         # Definición de botones personalizados
│  │  └─ Formularios/     # Modals para agregar/editar
│  ├─ cogs/               # Cog de comandos y eventos
│  │  ├─ Eventos.py        # Listeners de mensajes/voz/spam
│  │  ├─ Moderacion.py     # Comandos administrativos
│  │  └─ Offices.py        # Grupo principal de comandos
│  ├─ CommandModeracion/   # Lógica de comandos de moderación
│  ├─ CommandOffices/      # Lógica de comandos de oficinas
│  ├─ CommandPdf/          # Generación/gestión de PDFs
│  ├─ CommandSubida/       # (posible función de subida de archivos)
│  ├─ Declaraciones/       # Estados globales y vistas permanentes
│  ├─ Plantilla/           # HTML/recursos para PDF
│  └─ Services/           # Servicio web y cache de datos
├─ requirements.txt       # Dependencias Python
├─ README.md              # Este archivo
└─ env/                   # Entorno virtual (agnóstico)
```


## 🧭 Comandos principales

### Grupo `/offices`

| Comando | Descripción |
|--------|-------------|
| `/offices empezar <canalvoz>` | Inicia una office en un canal de voz. |
| `/offices terminar <id>` | Finaliza una office activa. |
| `/offices guardar <id>` | Mueve una office a revisión. |
| `/offices votar <id> tiempo>` | Crea una votación para una office activa. |
| `/offices ruleta <canalvoz>` | Inicia ruleta en un canal de voz. |
| `/offices mover <canal> <miembro>` | Traslada usuarios de voz sin pausar tiempo. |
| `/offices agregar <id> <estudiante>` | Abre modal para agregar/editar estudiante. |

#### Subgrupo `/offices editar`

- `/offices editar offices <id>` – Edita los datos de una office.
- `/offices editar estudiante <id_offices> <estudiante>` – Edita un registro de estudiante.

#### Subgrupo `/offices listar`

- `/offices listar estudiantes <id>` – Lista estudiantes de una office.
- `/offices listar offices` – Lista todas las offices activas o en revisión.

#### Subgrupo `/offices pdf`

- `/offices pdf obtener <nombre>` – Descarga un PDF generado de las offices.
- `/offices pdf eliminar <nombre>` – Elimina un PDF existente.

> ⚠️ Todos los comandos excepto `/offices ruleta` y `/offices mover` requieren
> que el usuario tenga un rol de staff configurado en `Estado.ListaDeRolesPermitidos`.

### Grupo `/administracion` (Moderación)

- `/administracion crear_form_registro` – Inserta en el canal un mensaje con botón
de registro automático para estudiantes nuevos.

### Interactivas automáticas

- Botones generados al entrar a un canal de voz para invitar al alumno a la office.
- Modal de registro/edición con validación de rango y duplicados.

---

## 🛡 Eventos y seguridad

- **Anti‑spam**: bloquea usuarios que envían más de 10 mensajes en 5 segundos.
- **Anti‑link**: elimina mensajes que contengan dominios conocidos por grabify, iplogger, etc.
- **Seguimiento de voz**: arranque/detención de temporizador cuando un estudiante entra
  o sale de un canal de office.
- **Filtro de staff**: ignora acciones de usuarios con roles `Staff` o `Admin Staff`.

---

## 🧩 Desarrollo y contribución

- El código usa una arquitectura modular; para añadir un nuevo comando cree un
  archivo en la carpeta `CommandX` correspondiente e importe en el `Cog`.
- Utilice el comando `python -m pyflakes .` o `pylint` para verificar errores de sintaxis.
- Para refactorizaciones de Python, el proyecto está preparado con herramientas de
  `pylance` y puede ejecutar `mcp_pylance_mcp_s_pylanceInvokeRefactoring` si es necesario.

---

## 📄 Licencia

Este proyecto está licenciado bajo la **MIT License**. Consulte el archivo `LICENSE`
para más detalles.

---

## 📚 Recursos adicionales

- [Manual del Bot Discord CS50](https://corc-my.sharepoint.com/:w:/g/personal/jessua_solis96u_std_uni_edu_ni/ER4crIBo7qBFlfJoXNcjQAAB3tdSh_thbUDUkZpzPUwHpw?rtime=p9AKb0u13Ug)

¡Gracias por usar el bot! 🎓

