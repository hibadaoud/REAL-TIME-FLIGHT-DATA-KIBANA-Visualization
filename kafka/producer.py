from confluent_kafka import Producer
import requests
import json
import time

# Kafka Producer Configuration
producer = Producer({'bootstrap.servers': 'localhost:9093'})

# Base URLs
flights_api_url = "https://airlabs.co/api/v9/flights?api_key=43f73f5a-f718-4c51-b41f-dd9bf2d1574b"
flight_details_api_url = "https://airlabs.co/api/v9/flight"

# API Key
api_key = "43f73f5a-f718-4c51-b41f-dd9bf2d1574b"
# Function to fetch flight details
def fetch_flight_details(flight_iata):
    try:
        url = f"{flight_details_api_url}?flight_iata={flight_iata}&api_key={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("response", {})
        else:
            print(f"Failed to fetch flight details for {flight_iata}: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Error fetching flight details: {e}")
        return {}

# Periodically fetch and publish data to Kafka
try:
    while True:
        # Fetch flights data from the API
        response = requests.get(flights_api_url)
        if response.status_code == 200:
            flights_data = response.json().get("response", [])  # Safely handle missing "response" key
            print(f"Fetched {len(flights_data)} flights")

            # Process each flight
            for flight in flights_data:
                flight_iata = flight.get("flight_iata", "")
                flight_details = fetch_flight_details(flight_iata) if flight_iata else {}

                # Merge flight data with its details
                combined_data = {**flight, **flight_details}

                # Publish combined data to Kafka
                producer.produce('flights', key=str(flight.get('hex', '')), value=json.dumps(combined_data))
                time.sleep(0.05)  # Small delay to prevent overwhelming Kafka

            # Ensure all messages are sent
            producer.flush()
        else:
            print(f"Failed to fetch flights data: {response.status_code}")

        # Sleep before fetching data again
        time.sleep(3600)  # Adjust as needed for your use case

except KeyboardInterrupt:
    print("\nShutting down gracefully...")
finally:
    # Ensure the producer is properly closed
    producer.flush()
