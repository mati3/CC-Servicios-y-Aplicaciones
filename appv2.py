from flask import Flask
import json
from flask import jsonify

from flask_caching import Cache

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


@app.route('/servicio/v2/prediccion/24horas/')
@cache.cached(timeout=50)
def pred_24Horas():
    return jsonify('pred_24Horas de v2'), 200


if __name__ == '__main__':
    app.run()
