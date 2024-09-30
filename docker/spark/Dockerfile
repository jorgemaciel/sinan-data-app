FROM bitnami/spark:latest

USER root
RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    apt-get clean

RUN pip3 install py4j pyarrow pandas delta-spark==3.2.0 minio

# Ignore WARN MetricsConfig
RUN touch /opt/bitnami/spark/conf/hadoop-metrics2-s3a-file-system.properties

COPY spark-defaults.conf /opt/bitnami/spark/conf/spark-defaults.conf
