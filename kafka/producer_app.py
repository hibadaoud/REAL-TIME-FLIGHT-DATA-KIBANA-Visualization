from confluent_kafka import Producer
import requests
import json
import time
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Kafka Producer Configuration
producer = Producer({'bootstrap.servers': 'kafka:9092'})

api_url = os.getenv('API_URL')

def delivery_report(err, msg):
    if err is not None:
        print(f"[ERROR] Message delivery failed: {err}")
    else:
        print(f"[INFO] Message delivered to {msg.topic()} [{msg.partition()}]") 

# Fetch data from the API
print("[INFO] Fetching data from API...")
response = requests.get(api_url)
print(f"[INFO] API responded with status: {response.status_code}")

if response.status_code == 200:
    print(f"[INFO] Received {len(response.json().get('response', []))} items.")
    data = response.json().get("response", [])

    for i, obj in enumerate(data):
        producer.produce('flights', key=str(obj.get('hex', '')), value=json.dumps(obj))
        if i == 0:
            print("[INFO] First Kafka message sent")  # Signal to Node.js
        time.sleep(0.01)  # Small delay to prevent overwhelming Kafka

    producer.flush()
    print("[INFO] All messages sent successfully.")
else:
    print(f"[ERROR] Failed to fetch data (Status Code: {response.status_code})")

        
