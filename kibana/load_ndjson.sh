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

# Kibana API URL
kibana_url="http://localhost:5601/api/saved_objects/_import"

# Ensure the file exists
if [[ ! -f "$file_path" ]]; then
    echo "Error: File '$file_path' does not exist."
    exit 1
fi

echo "Importing saved objects from: $file_path"

# Execute the import using curl
response=$(curl -v -X POST "$kibana_url" \
    -H "kbn-xsrf: true" \
    -H "Content-Type: multipart/form-data" \
    --form file=@"$file_path")

# Output the response
echo "Response: $response"
