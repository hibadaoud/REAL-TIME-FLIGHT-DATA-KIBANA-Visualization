#!/bin/bash

# Wait for Zookeeper to be ready
echo "Waiting for Zookeeper to start..."
while ! (echo > /dev/tcp/zookeeper/2181) &>/dev/null; do
  sleep 2
done

# Ensure the correct server.properties file is in place
if [ ! -f /opt/bitnami/kafka/config/server.properties ]; then
  echo "Renaming server.properties.original to server.properties..."
  mv /opt/bitnami/kafka/config/server.properties.original /opt/bitnami/kafka/config/server.properties
fi

# Start Kafka broker in the background
/opt/bitnami/scripts/kafka/run.sh &
    
# Wait for the Kafka broker to be ready
echo "Waiting for Kafka to start..."
sleep 20

# Create the topic 'flights'
kafka-topics.sh \
  --create \
  --topic flights \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1

echo "Topic 'flights' created."

# Wait to keep the container running
wait
