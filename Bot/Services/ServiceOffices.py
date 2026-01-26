import requests
from cachetools import TTLCache
from Clases import logs

class Services:

    _instancia = None
    def __new__(cls,TOKEN_SERVER: str ,API_KEY: str):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar(TOKEN_SERVER, API_KEY)
        return cls._instancia

    def _inicializar(self, TOKEN_SERVER: str ,API_KEY: str):
        self.___TOKEN_SERVER = TOKEN_SERVER
        self.___API_KEY = API_KEY
        self.CacheOffices = TTLCache(maxsize=20, ttl=3900)
        self.CacheVotos = TTLCache(maxsize=20, ttl=300)
        self.log = logs.Logs()

    def getCacheOffices(self):
        if len(self.CacheOffices.keys()) == 0:
            json = self.__getOffices()
            for key in json:
                self.CacheOffices[key] = json[key]
        
        print(self.CacheOffices)
        return self.CacheOffices

    def __getOffices(self, id: str = "") -> object:

        response = requests.get(url=f"{self.___TOKEN_SERVER}/offices/{id}", headers={"API_KEY": self.___API_KEY})
        if response.status_code != 200: 

            return None

        return response.json()


    def __getEstudiantes(self, id: str = "") -> object :
        """ Funcion que si no se le pasa el id retorna todas las offices, si se le para el argumento, pasa la de una en concreto """

        response = requests.get(url = f"{self.___TOKEN_SERVER}/offices/activas/estudiantes/{id}", headers={"API_KEY": self.___API_KEY})
        if response.status_code != 200: 
            return {"error":response.status_code}

        print(response.json())
        return response.json()


