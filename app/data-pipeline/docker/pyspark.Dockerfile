FROM apache/spark-py

SHELL ["/bin/bash", "-c"]

ARG USER_ID=1000
ARG USER_NAME=pyspark

ENV DEBIAN_FRONTEND=noninteractive

USER root

# RUN /opt/spark/bin/spark-submit --conf spark.driver.extraJavaOptions="-Divy.cache.dir=/tmp -Divy.home=/tmp" --packages org.apache.bahir:spark-sql-streaming-mqtt_2.11:2.3.1
# RUN /opt/spark/bin/spark-shell --packages org.apache.bahir:spark-sql-streaming-mqtt_2.11:2.3.1

CMD [ "/bin/bash" ]