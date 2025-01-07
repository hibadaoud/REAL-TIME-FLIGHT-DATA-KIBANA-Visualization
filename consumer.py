import os
from confluent_kafka import Consumer, KafkaException
import json

# Kafka Consumer Configuration
consumer = Consumer({
    'bootstrap.servers': 'localhost:9093' ,
    'group.id': 'my-group',                # Consumer group ID
    'auto.offset.reset': 'earliest'        # Start reading from the earliest message
})

# Path to save the data in kafka/consumer directory
output_dir = "."
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
output_file = os.path.join(output_dir, "fetched_data_try.json")

# Ensure the file exists and initialize it as an empty list if necessary
if not os.path.exists(output_file):
    with open(output_file, 'w') as f:
        json.dump([], f)  # Initialize with an empty JSON array

# Subscribe to the topic
consumer.subscribe(['flights'])  # Replace 'api' with your topic name if it's different

try:
    print("Listening for messages on the 'flights' topic...")
    while True:
        # Poll for a message (wait up to 1 second for new messages)
        msg = consumer.poll(1.0)

        if msg is None:
            # No message available
            continue
        if msg.error():
            # Handle any errors
            if msg.error().code() == KafkaException._PARTITION_EOF:
                # End of partition event
                print(f"Reached end of partition {msg.partition()}")
            else:
                print(f"Consumer error: {msg.error()}")
            continue

        # Successfully received a message
        data = json.loads(msg.value().decode('utf-8'))  # Decode and parse the message

        # Append the data to the JSON file
        with open(output_file, 'r+') as f:
            # Load existing data
            file_data = json.load(f)
            # Append the new data
            file_data.append(data)
            # Move the file pointer to the beginning
            f.seek(0)
            # Save updated data back to the file
            json.dump(file_data, f, indent=4)

        print(f"Saved message: {data}")

except KeyboardInterrupt:
    # Graceful shutdown on Ctrl+C
    print("\nShutting down consumer...")
finally:
    # Close the consumer
    consumer.close()
