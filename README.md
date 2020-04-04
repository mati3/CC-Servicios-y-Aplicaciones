# CC-Servicios-y-Aplicaciones

Hemos creado y desplegado un servicio Cloud Native completo, tenemos dos versiones de un mismo servicio.

[Enlace a la versión 1](https://github.com/mati3/CC-Servicios-y-Aplicaciones/tree/v1)

[Enlace a la versión 2](https://github.com/mati3/CC-Servicios-y-Aplicaciones/tree/v2)

El control de flujo de trabajo de nuestros servicios se ha realizado sobre AirFlow. Para ello ejecutamos sobre AirFlow el archivo [P2_CC.py](P2_CC.py)

Ambas versiones el resultado final es el mismo, la predicción del tiempo en 24, 48 y 72 horas de San Francisco. Se devuelven los datos en formato JSON.

En la primera versión se adquieren datos del tiempo de un repositorio, tras el tratamiento de los mismos se crea un modelo de predicción con ARIMA para predecir las siguientes 24, 48 o 72 horas respecto a la temperatura y humedad de San Francisco.

    Para acceder al servicio:

    http://localhost:8000/servicio/v1/prediccion/24horas/
    http://localhost:8000/servicio/v1/prediccion/48horas/
    http://localhost:8000/servicio/v1/prediccion/72horas/

En la segunda versión los datos se adquieren de una web externa “openweathermap”, la cual devuelve una predicción más amplia pero del mismo formato anterior, es decir, 24, 48 y 72 horas respecto a la temperatura y humedad de San Francisco.

    Para acceder al servicio:
    
    http://localhost:5000/servicio/v2/prediccion/24horas/
    http://localhost:5000/servicio/v2/prediccion/48horas/
    http://localhost:5000/servicio/v2/prediccion/72horas/

Para las API se levanta un contenedor docker donde se implanta el servicio a prestar.

