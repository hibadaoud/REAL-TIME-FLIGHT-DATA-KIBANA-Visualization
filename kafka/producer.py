from confluent_kafka import Producer
import requests
import json
import time

# Kafka Producer Configuration
producer = Producer({'bootstrap.servers': 'localhost:9093'})

api_url = "https://airlabs.co/api/v9/flights?api_key=ff090b3e-09ef-476c-939f-70d276978db3"

# Periodically fetch and publish data to Kafka
try:
    while True:
        # Fetch data from the API
        response = requests.get(api_url)
        print(response.status_code, response.text)  # Debug log

        if response.status_code == 200:
            # Parse the JSON response
            data = response.json().get("response", [])  # Safely handle missing "response" key
            print(data)
            
            # Publish each object in the response to the Kafka topic
            for obj in data:
                producer.produce('flights', key=str(obj.get('hex', '')), value=json.dumps(obj))
                time.sleep(0.05)  # Small delay to prevent overwhelming Kafka
            
            # Ensure all messages are sent
            producer.flush()
        else:
            print(f"Failed to fetch data from API (Status Code: {response.status_code})")
        
        # Sleep before fetching data again
        time.sleep(3600)  # Adjust as needed for your use case

except KeyboardInterrupt:
    print("\nShutting down gracefully...")
finally:
    # Ensure the producer is properly closed
    producer.flush()
