# WebserverApp/apiOh.py
from flask import Blueprint, jsonify

# NOTA: no se como pero asi funciona, NO TOCAR
from singleton import EG # type: ignore

apiOh = Blueprint('apiOh', __name__)

@apiOh.route("/OhActivas")
def listaOfficesActivas():
    offices_json = {k: v.to_dict() for k, v in EG.OfficesLista.items()}
    return jsonify(offices_json)

@apiOh.route("/OhRevision")
def listaOfficesRevision():
    offices_json = {k: v.to_dict() for k, v in EG.OfficesRevision.items()}
    return jsonify(offices_json)
