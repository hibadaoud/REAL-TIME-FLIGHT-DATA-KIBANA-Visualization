# Start from the Bitnami Spark image Spark
FROM bitnami/spark:3.2.4

# Switch to root to install packages
USER root

# Update the package list and install python3-pip, curl, telnet, and other utilities
RUN apt-get update && \
    apt-get install -y python3-pip curl telnet && \
    rm -rf /var/lib/apt/lists/*

# Install Scala 2.12
RUN curl -LO https://downloads.lightbend.com/scala/2.12.15/scala-2.12.15.tgz && \
    tar -xzvf scala-2.12.15.tgz -C /opt/ && \
    rm scala-2.12.15.tgz && \
    mv /opt/scala-2.12.15 /opt/scala

# Set up environment variables for Scala
ENV SCALA_HOME=/opt/scala
ENV PATH=$PATH:$SCALA_HOME/bin

# Create the checkpoints directories and ensure the non-root user has write access
RUN mkdir -p /opt/bitnami/spark/checkpoints/flights && \
    chown -R 1001:1001 /opt/bitnami/spark/checkpoints

RUN pip install spark pyspark

COPY ./spark/airports_external.csv /opt/bitnami/spark/airports_external.csv

COPY ./spark/spark-env.sh spark-master:/opt/bitnami/spark/conf/

# Copy spark file into a container
COPY ./spark/spark_stream.py /opt/bitnami/spark/spark_stream.py

# Switch back to the default user
USER 1001