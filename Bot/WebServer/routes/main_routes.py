from fastapi import APIRouter
from . import offices

app_router = APIRouter()

@app_router.get('/')
async def health():
    return "OK"

app_router.include_router(offices.router, prefix="/offices")