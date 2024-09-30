FROM apache/airflow:latest-python3.12

USER root
RUN apt-get update && \
    apt-get install -y gcc python3-dev openjdk-17-jdk procps wget make sudo && \
    apt-get clean

# Set JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64
RUN export JAVA_HOME

ADD ./docker/airflow/pysus /home/airflow/pysus

WORKDIR /home/airflow/pysus

RUN make install

WORKDIR /home/airflow

USER airflow

RUN pip install apache-airflow apache-airflow-providers-apache-spark apache-airflow-providers-amazon boto3 pyspark minio

RUN wget -P /home/airflow/.local/lib/python3.12/site-packages/pyspark/jars/ https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar

RUN wget -P /home/airflow/.local/lib/python3.12/site-packages/pyspark/jars/ https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar
