from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import pandas
from pandas import DataFrame
import csv

default_args = {
    'owner': 'Matilde Cabrera González',
    'depends_on_past': False,
    'start_date': days_ago(0),
    #'start_date': datetime.datetime(2020,09,10),
    'email': ['mati331@correo.ugr.es'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    #'retry_delay': timedelta(minutes=5),
}

#Inicialización del grafo DAG de tareas para el flujo de trabajo
dag = DAG(
    'P2_CC',
    default_args=default_args,
    description='Un grafo de tareas para la practica 2 de Cloud Computing Componentes y Servicios',
    schedule_interval=timedelta(days=1),#None
)

# Operadores o tareas # dejo los datos en tmp para no tener que descargar cada vez
PrepararEntorno = BashOperator(
		task_id='PrepararEntorno',
		depends_on_past=False,
		bash_command='mkdir /tmp/workflow/',
		dag=dag
		)

CapturaDatosA = BashOperator(
		task_id='CapturarDatosA',
		depends_on_past=False,
		bash_command='curl -o /tmp/workflow/humidity.csv.zip  https://raw.githubusercontent.com/manuparra/MaterialCC2020/master/humidity.csv.zip',
		dag=dag
		)

CapturaDatosB = BashOperator(
		task_id='CapturarDatosB',
		depends_on_past=False,
		bash_command='curl -o /tmp/workflow/temperature.csv.zip https://raw.githubusercontent.com/manuparra/MaterialCC2020/master/temperature.csv.zip',
		dag=dag
		)

DescomprimirDatosA = BashOperator(
		task_id='DescomprimirDatosA',
		depends_on_past=True,
		bash_command='unzip -od /tmp/workflow/ /tmp/workflow/humidity.csv.zip',
		dag=dag
		)

DescomprimirDatosB = BashOperator(
		task_id='DescomprimirDatosB',
		depends_on_past=True,
   		bash_command='unzip -od /tmp/workflow/ /tmp/workflow/temperature.csv.zip',
   		dag=dag
		)

# solo dos columnas, indexa por datetime, columnas = humidity y temperature
def limpiar_datos(path_file):
	df = pandas.read_csv(path_file+'humidity.csv', sep=',',index_col=0)
	df = df.rename(columns={'San Francisco':'humidity'})
	df = df.drop(df.columns[[0,1,3,4,5,6,7,8,9,10,11,12,13 ,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]], axis='columns')
	df = df[1:1500]
	
	df2 = pandas.read_csv(path_file+'temperature.csv', sep=',', index_col=0)
	df2 = df2.rename(columns={'San Francisco':'temperature'})
	df2 = df2.drop(df2.columns[[0,1,3,4,5,6,7,8,9,10,11,12,13 ,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35]], axis='columns')
	df2 = df2[1:1500]

	df3 = pandas.merge(df,df2,on='datetime')
	df3 = df3.dropna()# elimina filas con valores nulos
	df3.to_csv(path_file+'sanFrancisco.csv')

LimpiarUnirAB = PythonOperator(
		task_id='LimpiarUnirAB',
		depends_on_past=True,
		python_callable=limpiar_datos,
		op_args={'/tmp/workflow/'},
		dag=dag
		)

GenerarContenedorMongo = BashOperator(
    task_id='GenerarContenedorMongo',
    depends_on_past=True,
    bash_command="docker run -d -p 28900:27017 mongo:latest",
    dag=dag,
)

ImportarDatosMongo = BashOperator(
    task_id='ImportarDatosMongo',
    depends_on_past=True,
    bash_command="mongoimport -d BD1 -c sanFrancisco --type csv --file /tmp/workflow/sanFrancisco.csv --headerline --port 28900 --host localhost",
    dag=dag,
)

ClonarGit = BashOperator(
    task_id='ClonarGit',
    depends_on_past=True,
    bash_command="cd /tmp/workflow && git clone git@github.com:mati3/CC-Servicios-y-Aplicaciones.git",
    dag=dag,
)

GitV1 = BashOperator(
    task_id='GitV1',
    depends_on_past=True,
    bash_command="cd /tmp/workflow/CC-Servicios-y-Aplicaciones && git checkout v1",
    dag=dag,
)

BuildV1 = BashOperator(
    task_id='BuildV1',
    depends_on_past=True,
    bash_command='cd /tmp/workflow/CC-Servicios-y-Aplicaciones && docker build -f Dockerfile -t "mati331:ejer2_cc_v1" .',
    dag=dag,
)


RunV1 = BashOperator(
    task_id='RunV1',
    depends_on_past=True,
    bash_command="cd /tmp/workflow/CC-Servicios-y-Aplicaciones && docker run -p 8000:8000 --network='host' -t mati331:ejer2_cc_v1",
    dag=dag,
)

GitV2 = BashOperator(
    task_id='GitV2',
    depends_on_past=True,
    bash_command="cd /tmp/workflow/CC-Servicios-y-Aplicaciones && git checkout v2",
    dag=dag,
)

BuildV2 = BashOperator(
    task_id='BuildV2',
    depends_on_past=True,
    bash_command='cd /tmp/workflow/CC-Servicios-y-Aplicaciones && docker build -f Dockerfile -t "mati331:ejer2_cc_v2" .',
    dag=dag,
)


RunV2 = BashOperator(
    task_id='RunV2',
    depends_on_past=True,
    bash_command="cd /tmp/workflow/CC-Servicios-y-Aplicaciones && docker run -p 5000:5000 -t mati331:ejer2_cc_v2",
    dag=dag,
)

#Dependencias
PrepararEntorno >> [CapturaDatosA, CapturaDatosB] >> DescomprimirDatosA >> DescomprimirDatosB >> LimpiarUnirAB >> GenerarContenedorMongo >> ImportarDatosMongo >> ClonarGit >> GitV1 >> BuildV1 >> RunV1 >> GitV2 >> BuildV2 >> RunV2

