# Singleton que lleva toda la logica
from discord import Member
from Clases import EstudianteClass, OfficeClass

class EstadoGlobal:
    """ 
        OfficesLista -> { str(Id): Offices }, Es la estructura la cual guarda las offices que estan activas
        
        OfficesRevision -> { str(Id): Offices }, Es la estructura la cual guarda la offices que ya terminaron y esta en revision
        
        CanalesDeVoz -> { str(Canal): IdOffices }, Es la estructura que asocia una offices con un canal de voz
    """
        
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
        self.OfficesLista: dict[str,OfficeClass.Offices] = {} # { str(Id): Offices }, Es la estructura la cual guarda las offices que estan activas
        self.OfficesRevision: dict[str,OfficeClass.Offices] = {}   # { str(Id): Offices }, Es la estructura la cual guarda la offices que ya terminaron y esta en revision
        self.CanalesDeVoz: dict[str,str] = {}      # { str(Canal): IdOffices }, Es la estructura que asocia una offices con un canal de voz
        
        #[ Lista de roles que se excluyen o se aceptan en el servidor cs|web ]
        self.ListaDeRolesPermitidos: list[str] = ["Staff", "Admin", "Admin Staff", "Profesor", "staff", "Bot", "Bots"] 
        
    def getKeyCanalesDeVoz(self) -> list:
        """ Retorna Todas la key de los canales de voz """
        return list(self.CanalesDeVoz.keys())
    
    def getKeyOfficesLista(self) -> list:
        """ Retorna todas las keys de la offices que estan en lista (activas), la key es su Id """
        return list(self.OfficesLista.keys())
    
    def getKeyOfficesRevision(self) -> list:
        """ Retorna todas las keys de la offices que estan en revision, la key es su Id  """
        return list(self.OfficesRevision.keys())
    
    def getOffices(self, Id: str) -> OfficeClass.Offices | None:
        """ retorna una offices, ya sea activa o en revision """
        
        # Valida si es que esta en alguna parte de la offices, si no la encuentra retorna None
        if Id in self.getKeyOfficesLista():
            return self.OfficesLista[Id]
        if Id in self.getKeyOfficesRevision():
            return self.OfficesRevision[Id]

        # Si no encuentra nada retorna None
        return None
    
    def getOfficesTotalValues(self) -> list:
        """ Retorna una lista con todas la offices """
        lista = list(self.OfficesLista.values())
        lista += list(self.OfficesRevision.values())
        return lista
    
    
    def getEstudiante(self, Estudiante: Member | str, Id) -> EstudianteClass.Estudiante | None:
        """ Metodo para retornar un estudiante directo de la offices """
        office = self.getOffices(Id)
        
        if not office:
            # Si no encuentra la offices retorna None
            return None
        
        if type(Estudiante) == str:
            for User in office.Usuarios:
                
                # Valida por el Nombre (IdUsuario)
                if User.IdUsuario == Estudiante:
                    return User
            
            
            # Si no lo encuentra Retorna None
            return None
        
        if type(Estudiante) ==  Member:
            for User in office.Usuarios:
                
                # Valida por el id de discord
                if Estudiante.id == User.IdDiscord:
                    return User
                
            # Si no lo encuentra Retorna None
            return None
        
        # Caso base de que si XD
        return None
        