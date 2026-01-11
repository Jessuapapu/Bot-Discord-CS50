from fastapi import APIRouter, HTTPException

from Declaraciones import EstadoGlobal
router = APIRouter()

SIG = EstadoGlobal.EstadoGlobal()

@router.get("/")
async def obtener_offices():
    return SIG.to_dict()

@router.get("/activas/estudiantes")
async def obtener_offices():
    return SIG.to_DictActivasEstudiantes()

@router.get("/activas/informacion")
async def obtener_officesInformacion():  
    return SIG.to_DictInformacion()


@router.get("/get/{id_Offices}")
async def obtener_officesEsoecifica(id_Offices: str):
    return SIG.getOffices(id_Offices) if SIG.getOffices(id_Offices) is not None else HTTPException(status_code=404,detail="Offices no encontrada")