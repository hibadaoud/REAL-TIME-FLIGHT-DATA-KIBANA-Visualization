#!/bin/bash

. /opt/bitnami/scripts/liblog.sh

# Function to check if Kibana is ready
check_kibana_ready() {
    until curl -s http://kibana-cntr:5601; do
        echo "Waiting for Kibana..."
        sleep 3
    done
    echo "Kibana is ready."
}

check_kibana_ready
sleep 10

# Path to the NDJSON file
file_path="/usr/share/kibana/scripts/export.ndjson"
kibana_url="http://localhost:5601/api/saved_objects/_import"
find_url="http://localhost:5601/api/saved_objects/index-pattern/23cd45e3-6e92-4e1e-a11c-7f3a3a708bf8"

# Ensure the file exists
if [[ ! -f "$file_path" ]]; then
    echo "Error: File '$file_path' does not exist."
    exit 1
fi

echo "Checking if the dashboard already exists"

# Check if the specific object already exists
response=$(curl -s -o /dev/null -w "%{http_code}" -X GET "$find_url" -H "kbn-xsrf: true")
echo "$response"

if [[ "$response" -eq 200 ]]; then
    echo "The dashboard already exists. Skipping import."
    exit 0
fi

echo "Importing saved objects from: $file_path"

# Execute the import using curl
import_response=$(curl -s -X POST "$kibana_url" \
    -H "kbn-xsrf: true" \
    -H "Content-Type: multipart/form-data" \
    --form file=@"$file_path")

# Output the response
echo "Response: $import_response"
