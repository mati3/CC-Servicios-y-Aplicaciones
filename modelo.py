import pandas
from pandas import DataFrame
import json
import requests
from datetime import datetime

def to_json(modelo):
    datos ='{"San Francisco ":{'
    contador = 0
    for h in modelo["humidity"]:
        if contador != len(modelo["humidity"])-1:
            datos +='"Hora '+ str(contador) + '" : { ' +'"humidity" : '+ str(h)+', "temperature" : '+ str(modelo["temperature"][contador])+' },'
        else:
            datos +='"Hora '+ str(contador) + '" : { ' +'"humidity" : '+ str(h)+', "temperature" : '+ str(modelo["temperature"][contador])+' }'
        contador += 1
    datos +="} }"
    return datos


def crearModeloDesdeOtraWeb(pds):

    df = requests.get(url = "https://samples.openweathermap.org/data/2.5/forecast/hourly?lat=35&lon=139&appid=b6907d289e10d714a6e88b30761fae22")
    datos = df.json()
    # se normalizan los datos
    dataframe = pandas.io.json.json_normalize(datos['list'])

    fechahoy = datetime.now() 
    indice = pandas.date_range(fechahoy, periods=pds, freq='H')

    salida= pandas.DataFrame(index=indice, columns=['humidity',"temperature"])
    salida['temperature']=dataframe['main.temp'].head(pds).values
    salida['humidity']=dataframe['main.humidity'].head(pds).values    

    return to_json(salida)

crearModeloDesdeOtraWeb(24)
