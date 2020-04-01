import pandas
from pandas import DataFrame
import csv
import numpy
import pmdarima as pm
import json

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

def crearModeloDesdeFile(pd):

    df = pandas.read_csv('/home/mati/workflow/sanFrancisco.csv')

    modelTemperature = pm.auto_arima(df['temperature'], start_p=1, start_q=1,
                        test='adf',       # use adftest to find optimal 'd'
                        max_p=3, max_q=3, # maximum p and q
                        m=1,              # frequency of series
                        d=None,           # let model determine 'd'
                        seasonal=False,   # No Seasonality
                        start_P=0, 
                        D=0, 
                        trace=True,
                        error_action='ignore',  
                        suppress_warnings=True, 
                        stepwise=True)
    
    modelHumidity = pm.auto_arima(df['humidity'], start_p=1, start_q=1,
                        test='adf',       # use adftest to find optimal 'd'
                        max_p=3, max_q=3, # maximum p and q
                        m=1,              # frequency of series
                        d=None,           # let model determine 'd'
                        seasonal=False,   # No Seasonality
                        start_P=0, 
                        D=0, 
                        trace=True,
                        error_action='ignore',  
                        suppress_warnings=True, 
                        stepwise=True)

    salida = pandas.DataFrame(columns=['humidity','temperature'])
    # Forecast
    #n_periods = 24 # One day
    fcTemperature, confint = modelTemperature.predict(n_periods=pd, return_conf_int=True)
    salida['temperature'] = numpy.array(fcTemperature)
    # fc contains the forecasting for the next 24 hours.

    fcHumidity, confint = modelHumidity.predict(n_periods=pd, return_conf_int=True)
    salida['humidity'] = fcHumidity
    # fc contains the forecasting for the next 24 hours.

    return to_json(salida)


#crearModeloDesdeFile(24)


import pymongo
from pymongo import MongoClient


def crearModeloDesdeMongo(periods):

    client = MongoClient("mongodb://0.0.0.0:28900")
    db = client["BD1"] # show databases;
    col= db["sanFrancisco"] # show collections;
    df = pandas.DataFrame(list(col.find()))

    modelTemperature = pm.auto_arima(df['temperature'], start_p=1, start_q=1,
                        test='adf',       # use adftest to find optimal 'd'
                        max_p=3, max_q=3, # maximum p and q
                        m=1,              # frequency of series
                        d=None,           # let model determine 'd'
                        seasonal=False,   # No Seasonality
                        start_P=0, 
                        D=0, 
                        trace=True,
                        error_action='ignore',  
                        suppress_warnings=True, 
                        stepwise=True)
    
    modelHumidity = pm.auto_arima(df['humidity'], start_p=1, start_q=1,
                        test='adf',       # use adftest to find optimal 'd'
                        max_p=3, max_q=3, # maximum p and q
                        m=1,              # frequency of series
                        d=None,           # let model determine 'd'
                        seasonal=False,   # No Seasonality
                        start_P=0, 
                        D=0, 
                        trace=True,
                        error_action='ignore',  
                        suppress_warnings=True, 
                        stepwise=True)

    #periods = 24 # One day
    salida = pandas.DataFrame(columns=['humidity','temperature'])

    fcTemperature, confint = modelTemperature.predict(n_periods=periods, return_conf_int=True)
    salida['temperature'] = numpy.array(fcTemperature)

    fcHumidity, confint = modelHumidity.predict(n_periods=periods, return_conf_int=True)
    salida['humidity'] = fcHumidity
    
    return to_json(salida)

#crearModeloDesdeMongo(24)
