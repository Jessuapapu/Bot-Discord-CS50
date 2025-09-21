# webserver.py
from flask import Flask
from flask_cors import CORS
from Declaraciones.EstadoGlobal import EstadoGlobal


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Botsito de CS50 o WEB JAJJAJAJ'

@app.route("/api/OhActivas")
def listaOfficesActivas():

    EG = EstadoGlobal()
    dicc = {}
    for key, oh in zip(EG.getKeyOfficesLista(), EG.getOfficesListaValues()):
        print(key,oh)
        dicc[key] = oh.Id, oh.HoraCreacion
    return dicc
