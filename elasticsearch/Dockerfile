FROM bitnami/elasticsearch:8.8.2

# Install Python and Elasticsearch Python Client
USER root
RUN apt-get update && apt-get install -y python3 python3-pip \
    && pip3 install elasticsearch==8.8.2 \
    && chown -R 1001:1001 /opt/bitnami/elasticsearch \
    && chmod 775 /opt/bitnami/elasticsearch

# Copy custom scripts
COPY create_index_elastic.py /usr/share/elasticsearch/scripts/create_index_elastic.py
COPY custom_startup.sh /usr/share/elasticsearch/scripts/custom_startup.sh

# Make the startup script executable
RUN chmod +x /usr/share/elasticsearch/scripts/custom_startup.sh

# Switch to non-root user
USER 1001

# Set default entrypoint and command
ENTRYPOINT [ "/opt/bitnami/scripts/elasticsearch/entrypoint.sh" ] 
CMD [ "/usr/share/elasticsearch/scripts/custom_startup.sh" ]
