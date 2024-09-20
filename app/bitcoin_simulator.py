import json
import time
import requests
from kafka import KafkaProducer
from datetime import datetime


# Function to fetch 
def fetch_bitcoin_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin',
        'vs_currencies': 'usd',
        'include_market_cap': 'true',
        'include_24hr_vol': 'true'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "timestamp": str(datetime.now()),
            "buy_price": data["bitcoin"]["usd"],  
            "sell_price": data["bitcoin"]["usd"] - 100, #Simulating fake sell price
            "volume": data["bitcoin"]["usd_24h_vol"]
        }
    else:
        return None

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',  # Kafka service inside Docker
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Kafka topic name
topic_name = 'bitcoin_data_stream'


while True:
    bitcoin_data = fetch_bitcoin_data()
    if bitcoin_data:
        producer.send(topic_name, value=bitcoin_data)
        print(f"Published: {bitcoin_data}")
    else:
        print("Failed to fetch Bitcoin data")
    
    time.sleep(60)
