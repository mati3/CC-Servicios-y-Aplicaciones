from flask import Flask
import json
from flask import jsonify
from flask_caching import Cache
from modelo import crearModeloDesdeMongo
#from modelo import crearModeloDesdeFile
config = {
    "DEBUG": True,          
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@app.route('/')
@cache.cached(timeout=50)
def hello_world():
    return jsonify('Hello, World !'), 200


@app.route('/servicio/v1/prediccion/24horas/')
@cache.cached(timeout=50)
def pred_24Horas():
    modelo = crearModeloDesdeMongo(24)
    return modelo, 200

@app.route('/servicio/v1/prediccion/48horas/')
@cache.cached(timeout=50)
def pred_48Horas():
    modelo = crearModeloDesdeMongo(48)
    return modelo, 200

@app.route('/servicio/v1/prediccion/72horas/')
@cache.cached(timeout=50)
def pred_72Horas():
    modelo = crearModeloDesdeMongo(72)
    return modelo, 200

if __name__ == '__main__':
    app.run()
