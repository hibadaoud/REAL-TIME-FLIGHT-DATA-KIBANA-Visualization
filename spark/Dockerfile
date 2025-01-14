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
ENV SCALA_HOME /opt/scala
ENV PATH $PATH:$SCALA_HOME/bin

# Create the checkpoints directories and ensure the non-root user has write access
RUN mkdir -p /opt/bitnami/spark/checkpoints/flights && \
    chown -R 1001:1001 /opt/bitnami/spark/checkpoints

RUN pip install spark pyspark

# Pre-download Spark dependencies
# RUN mkdir -p /opt/bitnami/spark/jars && \
#     curl -L -o /opt/bitnami/spark/jars/spark-sql-kafka-0-10_2.12-3.2.4.jar https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.2.4/spark-sql-kafka-0-10_2.12-3.2.4.jar && \
#     curl -L -o /opt/bitnami/spark/jars/kafka-clients-2.8.1.jar https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/2.8.1/kafka-clients-2.8.1.jar && \
#     curl -L -o /opt/bitnami/spark/jars/spark-token-provider-kafka-0-10_2.12-3.2.4.jar https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.2.4/spark-token-provider-kafka-0-10_2.12-3.2.4.jar && \
#     curl -L -o /opt/bitnami/spark/jars/hadoop-client-api-3.3.1.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-client-api/3.3.1/hadoop-client-api-3.3.1.jar && \
#     curl -L -o /opt/bitnami/spark/jars/hadoop-client-runtime-3.3.1.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-client-runtime/3.3.1/hadoop-client-runtime-3.3.1.jar && \
#     curl -L -o /opt/bitnami/spark/jars/snappy-java-1.1.8.4.jar https://repo1.maven.org/maven2/org/xerial/snappy/snappy-java/1.1.8.4/snappy-java-1.1.8.4.jar

# Copy create index file into app directory into a spark container
COPY airports_external.csv /opt/bitnami/spark/airports_external.csv

COPY spark-env.sh spark-master:/opt/bitnami/spark/conf/

# Copy spark file into a container
COPY spark_stream.py /opt/bitnami/spark/spark_stream.py

# Switch back to the default user
USER 1001