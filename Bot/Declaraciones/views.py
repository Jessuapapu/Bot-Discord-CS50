from discord import ui
from Clases.Botones import BotonesRegistro
import asyncio

    
class viewsPersistentes:
    _instancia = None
    _lock = asyncio.Lock()
    
    async def __new__(cls, *agrs, **kwargs):
        if cls._instancia is None:
          async with cls._lock:
              if cls._instancia is None:
                    cls._instancia = super().__new__(cls)
                    await cls._instancia._async_init(*agrs, **kwargs)
        return cls._instancia 
    
    async def CrearVistaPersistente(self, listaBotones):
        view = ui.View(timeout = None)
        for boton in listaBotones:
            view.add_item(boton)
        return view

    async def _async_init(self,*agrs, **kwargs):
        self.vistaRegistro = await self.CrearVistaPersistente([BotonesRegistro.botonesRegistro()])
