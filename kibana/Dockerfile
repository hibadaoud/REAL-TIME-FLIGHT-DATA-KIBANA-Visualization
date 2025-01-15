FROM bitnami/kibana:8.8.2

USER root

RUN apt-get update && \
    apt-get install -y bash curl jq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    chown -R 1001:1001 /opt/bitnami/kibana && \
    chmod 775 /opt/bitnami/kibana


COPY kibana/export.ndjson /usr/share/kibana/scripts/export.ndjson
COPY kibana/load_ndjson.sh /usr/share/kibana/scripts/load_ndjson.sh
COPY kibana/custom_cmd.sh /usr/share/kibana/scripts/custom_cmd.sh

RUN chmod +x /usr/share/kibana/scripts/custom_cmd.sh

USER 1001

ENTRYPOINT [ "/opt/bitnami/scripts/kibana/entrypoint.sh" ]
CMD [ "/usr/share/kibana/scripts/custom_cmd.sh" ]