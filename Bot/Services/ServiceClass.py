import requests
from Declaraciones import EstadoGlobal
from Clases import logs, OfficeClass, EstudianteClass

class Services:

    _instancia = None
    async def __new__(cls,TOKEN_SERVER: str ,API_KEY: str, DISCORD_SERVER_ID: str):

        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            await cls._instancia._inicializar(TOKEN_SERVER, API_KEY,DISCORD_SERVER_ID)

        return cls._instancia


    async def _inicializar(self, TOKEN_SERVER: str, API_KEY: str, DISCORD_SERVER_ID: str):
        self.___TOKEN_SERVER = TOKEN_SERVER
        self.___API_KEY = API_KEY
        self.___DISCORD_SERVER_ID = DISCORD_SERVER_ID

        self.EG =  EstadoGlobal.EstadoGlobal()
        self.log = logs.Logs()

        try:
            codigo = requests.get(f"{TOKEN_SERVER}/").status_code
            if codigo != 200:
                self.log.add_log(f"ERROR OBTENIDO AL TRATAR DE CONECTARSE AL SERVER {codigo}", "ERROR")
                raise ValueError(f"ERROR OBTENIDO AL TRATAR DE CONECTARSE AL SERVER {codigo}")

            self.log.add_log(f"CONECTADO AL SERVER {codigo}", "INFO")    
            print("CONECTADO AL SERVIDOR")

        except requests.exceptions.ConnectionError as e:
            self.log.add_log(F"ERROR {e.strerror} o ERROR AL CONECTARSE AL SERVIDOR","ERROR")
            print("ERROR AL CONECTARSE AL SERVIDOR")

        except Exception as e:
            self.log.add_log(f"ERROR OBTENIDO AL TRATAR DE CONECTARSE AL SERVER {codigo}","ERROR")

        await self.getCacheOffices()




    async def getCacheOffices(self):

        jsonOffices = await self.__getOffices() 
        
        if jsonOffices is None:
            self.log.add_log(f"NO SE PUDO CARGAR LA INFORMACION OBTENIDA","INFO")
            return None
        
        for key in jsonOffices:
            if key in self.EG.OfficesLista.keys() or self.EG.OfficesRevision.keys():
                continue    
            
            estudiantes = self.___formatoestudiantes(jsonOffices[key]["Usuarios"])
            offices = OfficeClass.Offices(key, jsonOffices[key]["IdUsuario"],
                                                               estudiantes, jsonOffices[key]["bloque"]
                                                               ,jsonOffices[key]["canal"], jsonOffices[key]["staff"])

            if jsonOffices[key]["Estado"] is True:
                offices.Estado = True
                self.EG.OfficesLista[key] = offices
            
            elif jsonOffices[key]["Estado"] is False:
                offices.Estado = False
                self.EG.OfficesRevision[key] = offices
            
            else:
                self.log.add_log(f"ERROR AL CARGAR LA INFORMACION DE LA OFFICES {key}, no se sabe el estado","ERROR")

        print(self.EG.OfficesLista)
        return
    
    # TODO(refactorizar) ----- 
    async def getCacheEstudiantes(self):

        jsonEstudiantes = await self.__getEstudiantes()
        if jsonEstudiantes is None:
            self.log.add_log(F"NO SE PUDO CARGAR LA INFORMACION","INFO")
            return None
        
        for key in jsonEstudiantes:
            self.CacheEstudiantes[key] = self.___formatoestudiantes(jsonEstudiantes["Usuarios"]) 

        return self.CacheEstudiantes


    async def ___formatoestudiantes(self, lista: list) -> list[EstudianteClass.Estudiante]:
        ListaEstudiantes = []
        
        for estudiante in lista:
            try:
                estu = EstudianteClass.Estudiante(estudiante["IdUsuario"], estudiante["IdDiscord"], estudiante["IdOffice"],
                                                               estudiante["grupo"])
                ListaEstudiantes.append(estu)
            except Exception as e:
                self.log(f"ERROR AL OBTENER ESTUDIANTE, {str(e)}","ERROR")
        
        return ListaEstudiantes


    async def __getOffices(self, id: str = "") -> object | None:
        try:
            response = requests.get(url=f"{self.___TOKEN_SERVER}/offices/{id}", headers={"API_KEY": self.___API_KEY})
            if response.status_code != 200: 
                self.log.add_log(f"respuesta de error obtenida del servicio web: {response.status_code}","ERROR")
                return None

        except requests.exceptions.ConnectionError as e:
            self.log.add_log(f"No hubo respuesta del servicio web: {e.strerror}","ERROR")
            return None

        return response.json()


    async def __getEstudiantes(self, id: str = "") -> object | None :
        """ Funcion que si no se le pasa el id retorna todas las offices, si se le para el argumento, pasa la de una en concreto """
        try:
            response = requests.get(url = f"{self.___TOKEN_SERVER}/offices/activas/estudiantes/{id}", headers={"API_KEY": self.___API_KEY})
            if response.status_code != 200: 
                self.log.add_log(f"respuesta de error obtenida del servicio web: {response.status_code}","ERROR")
                return None
        
        except requests.exceptions.ConnectionError as e:
            self.log.add_log(f"No hubo respuesta del servicio web: {str(e)}","ERROR")
            return None

        return response.json()
    
    async def __fetch_UsuarioDiscord(self, user_id: str):
        # Inyectamos el guild_id específico en la URL
            url = f"https://discord.com/api/v10/guilds/{self.DISCORD_SERVER_ID}/members/{user_id}"

            headers = {
                "Authorization": f"Bot {self.___DISCORD_TOKEN}", # El token del bot sigue siendo global
                "Content-Type": "application/json"
            }

            try:
                response = requests.get(url, headers=headers, timeout=3)

                if response.status_code == 200:
                    data = response.json()
                    nickname = data.get('nick')
                    user_data = data.get('user', {})
                    global_name = user_data.get('global_name')
                    username = user_data.get('username')

                    # Misma lógica de prioridad
                    return nickname if nickname else (global_name if global_name else username)

                elif response.status_code == 404:
                    return "No encontrado en Server"
                else:
                    self.log.add_log(f"API Error {response.status_code}", "WARN")
                    return "Error API"

            except Exception as e:
                self.log.add_log(f"Error conectando a Discord: {str(e)}", "ERROR")
                return "Error Conexión"