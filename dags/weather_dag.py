from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import json 
import requests
from kafka import KafkaProducer

default_args = {
    'owner' : 'Erion Mediu',
    'start_date' : datetime(2025, 3, 20, 10 , 00)
}


def stream_data():
    mykey = 'My api key'
    producer = KafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        max_request_size=1000000  # optional, avoid overly large messages
        )


    response = requests.get('http://api.weatherapi.com/v1/current.json?key={mykey}&q=Amsterdam&aqi=no')
    response = response.json()

    output = {
        'current_time': response['location']['localtime'],
        'city_name': response['location']['name'],
        'last_updated_time_formated': datetime.fromtimestamp(response['current']['last_updated_epoch']).strftime('%H:%M'),
        'temp_c': response['current']['temp_c'],
        'wind_kph': response['current']['wind_kph'],
        'precip_mm': response['current']['precip_mm'],
        'feelslike_c': response['current']['feelslike_c']
        }
    
    producer.send('weather_topic', value=output)
    producer.flush()


with DAG('automatic_pull',
         default_args=default_args,
         schedule_interval='*/6 * * * *',  # every minute
         catchup=False) as dag:
    
    streaming_task = PythonOperator(
        task_id='stream_weather_data',
        python_callable=stream_data
    )
