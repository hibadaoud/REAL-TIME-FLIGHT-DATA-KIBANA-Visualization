#!/bin/bash

# Run the setup script to ensure Elasticsearch is properly initialized
/opt/bitnami/scripts/elasticsearch/setup.sh

# Start Elasticsearch in the background
/opt/bitnami/scripts/elasticsearch/run.sh &

# Wait for Elasticsearch to be ready
while true; do
    curl -s http://localhost:9200 && break
    sleep 1
done

# Run the index creation script
python3  /usr/share/elasticsearch/scripts/create_index_elastic.py

# Keep the container running
tail -f /dev/null
