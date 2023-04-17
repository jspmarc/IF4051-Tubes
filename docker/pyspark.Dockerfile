FROM apache/spark-py:v3.4.0

USER root

ARG USER_ID=1000
ARG USER_NAME=spark

RUN useradd -M -u ${USER_ID} ${USER_NAME}

USER ${USER_NAME}

CMD $SPARK_HOME/bin/spark-submit --packages "org.apache.bahir:spark-streaming-mqtt_2.11:2.4.0" --conf spark.driver.extraJavaOptions="-Divy.cache.dir=/tmp -Divy.home=/tmp" /pyspark/main.py
