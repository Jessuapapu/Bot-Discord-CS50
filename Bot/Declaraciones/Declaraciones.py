# Singleton que lleva toda la logica

class EstadoGlobal:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
        self.OfficesLista = {}      # { str(Id): Offices  }
        self.CanalesDeVoz = {}      # { str(Canal): IdOffices }
        self.OfficesRevision = {}   # { str(Id): Offices  }
        
    def getKeyCanalesDeVoz(self):
        return list(self.CanalesDeVoz.keys())
    
    def getKeyOfficesLista(self):
        return list(self.OfficesLista.keys())
    
    def getKeyOfficesRevision(self):
        return list(self.OfficesRevision.keys())