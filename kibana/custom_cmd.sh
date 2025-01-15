#!/bin/bash


. /opt/bitnami/scripts/liblog.sh

# Run the setup script
info "************************************ Starting kibana setup ************************************"
/opt/bitnami/scripts/kibana/setup.sh 
info "************************************ kibana setup finished! ************************************"

# Run the default script script
info ""
/opt/bitnami/scripts/kibana/run.sh &

# Execute the Python script
info "************************************ Exporting data  ************************************"

/usr/share/kibana/scripts/load_ndjson.sh

info "************************************ Exporting data DONE! ************************************"


# Keep the container running
# tail -f /dev/null
wait