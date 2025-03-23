# 🌤️ Real-Time Weather Stream to Telegram using Airflow + Kafka

This project streams weather data every 15 minutes via Kafka and sends updates to a Telegram chat using Apache Airflow.

---

## 🔧 Setup Instructions (Local)

### 1. Clone the repository

git clone https://github.com/erionmediu/Weather-straming.git
cd weather-stream



### 2. Create a virtual environment (for running Kafka producer/test)
python -m venv venv
source venv/bin/activate        # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt


### 3. Start the entire stack
docker compose up --build


### 4. Access the Airflow UI

    Open browser: http://localhost:8080

    Login: admin / admin


### 5. Expected Folder Structure
    weather-stream/
    ├── dags/
    │   ├── weather_dag.py
    │   └── telegram_weather.py
    ├── docker-compose.yml
    ├── requirements.txt
    └── README.md


### 6. 💬 Telegram Setup

    Create a bot via BotFather

    Copy the token and update it in telegram_weather.py

    Send a message to the bot from your Telegram account

    Get your chat ID by calling:
    https://api.telegram.org/bot<your_token>/getUpdates

```bash





