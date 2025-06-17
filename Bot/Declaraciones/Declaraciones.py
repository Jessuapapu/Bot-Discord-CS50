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
        self.CanalesDeVoz = []      # Canales de voz monitoreados
        self.ContadoresActivos = {} # { str(user.id): (Estudiante, tarea) }
        
