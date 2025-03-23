from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from kafka import KafkaConsumer
import json
import requests

# Replace with your actual values
TELEGRAM_TOKEN = 'mytoken'
CHAT_ID = 'myid'

default_args = {
    'owner': 'Erion Mediu',
    'start_date': datetime(2025, 3, 20, 10, 0)
}

def send_latest_weather():
    consumer = KafkaConsumer(
        'weather_topic',
        bootstrap_servers='kafka:9092',
        auto_offset_reset='latest',
        enable_auto_commit=False,
        group_id='telegram_notifier',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for msg in consumer:
        weather = msg.value
        break  # read only 1 latest msg

    text = (
        f"🌤️ Weather Update\n"
        f"📍 {weather['city_name']} at {weather['current_time']}\n"
        f"🌡️ Temp: {weather['temp_c']}°C (Feels like {weather['feelslike_c']}°C)\n"
        f"🌬️ Wind: {weather['wind_kph']} kph\n"
        f"🌧️ Precip: {weather['precip_mm']} mm"
    )

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text}
    )

with DAG('send_weather_telegram',
         default_args=default_args,
         schedule_interval='* * * * *',  # every minute
         catchup=False) as dag:

    send_telegram = PythonOperator(
        task_id='send_weather_update',
        python_callable=send_latest_weather
    )
