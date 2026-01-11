from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.main_routes import app_router

# App declaracion 
app = FastAPI()


# declaracion de rutas
app.include_router(app_router)

# Configuración de CORS para FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)





# declaracion de Singleton
#   SIG = EstadoGlobal.EstadoGlobal()






