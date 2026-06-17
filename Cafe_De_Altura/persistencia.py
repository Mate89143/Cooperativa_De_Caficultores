import json
from modelos import Asociado, Finca, Cosecha, Venta

ARCHIVO = "datos.json"

def guardar(s):
    with open(ARCHIVO, "w") as f:
        json.dump({
            "asociados": {k: vars(v) for k, v in s._asociados.items()},
            "fincas": {k: vars(v) for k, v in s._fincas.items()},
            "cosechas": {k: vars(v) for k, v in s._cosechas.items()},
            "ventas": {k: vars(v) for k, v in s._ventas.items()}
        }, f, indent=2)

def cargar(s):
    try:
        with open(ARCHIVO, "r") as f:
            d = json.load(f)
            s._asociados = {k: Asociado(**v) for k, v in d["asociados"].items()}
            s._fincas = {k: Finca(**v) for k, v in d["fincas"].items()}
            s._cosechas = {k: Cosecha(**v) for k, v in d["cosechas"].items()}
            s._ventas = {k: Venta(**v) for k, v in d["ventas"].items()}
    except FileNotFoundError:
        pass