import requests
from Declaraciones import EstadoGlobal
from Clases import logs, OfficeClass, EstudianteClass

class Services:

    _instancia = None
    def __new__(cls,TOKEN_SERVER: str ,API_KEY: str):

        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar(TOKEN_SERVER, API_KEY)

        return cls._instancia


    def _inicializar(self, TOKEN_SERVER: str, API_KEY: str):
        self.___TOKEN_SERVER = TOKEN_SERVER
        self.___API_KEY = API_KEY

        self.EG = EstadoGlobal.EstadoGlobal()
        self.log = logs.Logs()

        try:
            codigo = requests.get(f"{TOKEN_SERVER}/").status_code
            if codigo != 200:
                self.log.add_log(f"ERROR OBTENIDO AL TRATAR DE CONECTARSE AL SERVER {codigo}", "ERROR")
                pass

            self.log.add_log(f"CONECTADO AL SERVER {codigo}", "INFO")    

        except requests.exceptions.ConnectionError as e:
            self.log.add_log(F"ERROR {e.strerror} o ERROR AL CONECTARSE AL SERVIDOR","ERROR")
            print("ERROR AL CONECTARSE AL SERVIDOR")


    def getCacheOffices(self):

        jsonOffices = self.__getOffices() 
        
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
    

    def getCacheEstudiantes(self):

        jsonEstudiantes = self.__getEstudiantes()
        if jsonEstudiantes is None:
            self.log.add_log(F"NO SE PUDO CARGAR LA INFORMACION","INFO")
            return None
        
        for key in jsonEstudiantes:
            self.CacheEstudiantes[key] = self.___formatoestudiantes(jsonEstudiantes["Usuarios"]) 

        return self.CacheEstudiantes


    def ___formatoestudiantes(self, lista: list) -> list[EstudianteClass.Estudiante]:
        ListaEstudiantes = []
        
        for estudiante in lista:
            try:
                estu = EstudianteClass.Estudiante(estudiante["IdUsuario"], estudiante["IdDiscord"], estudiante["IdOffice"],
                                                               estudiante["grupo"])
                ListaEstudiantes.append(estu)
            except Exception as e:
                self.log(f"ERROR AL OBTENER ESTUDIANTE, {str(e)}","ERROR")
        
        return ListaEstudiantes


    def __getOffices(self, id: str = "") -> object | None:
        try:
            response = requests.get(url=f"{self.___TOKEN_SERVER}/offices/{id}", headers={"API_KEY": self.___API_KEY})
            if response.status_code != 200: 
                self.log.add_log(f"respuesta de error obtenida del servicio web: {response.status_code}","ERROR")
                return None

        except requests.exceptions.ConnectionError as e:
            self.log.add_log(f"No hubo respuesta del servicio web: {e.strerror}","ERROR")
            return None

        return response.json()


    def __getEstudiantes(self, id: str = "") -> object | None :
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