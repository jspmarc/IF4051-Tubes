FROM apache/spark-py:v3.4.0

ARG USER_ID=1000
ARG USER_NAME=spark

USER root

RUN useradd -M -u ${USER_ID} ${USER_NAME}

ADD https://repo1.maven.org/maven2/org/apache/bahir/spark-streaming-mqtt_2.11/2.4.0/spark-streaming-mqtt_2.11-2.4.0.jar \
	${SPARK_HOME}/jars

ADD https://repo1.maven.org/maven2/org/eclipse/paho/org.eclipse.paho.client.mqttv3/1.1.0/org.eclipse.paho.client.mqttv3-1.1.0.jar \
	${SPARK_HOME}/jars

ADD https://repo1.maven.org/maven2/org/spark-project/spark/unused/1.0.0/unused-1.0.0.jar \
	${SPARK_HOME}/jars

ADD https://repo1.maven.org/maven2/org/eclipse/paho/org.eclipse.paho.client.mqttv3/1.1.0/org.eclipse.paho.client.mqttv3-1.1.0.jar \
	${SPARK_HOME}/jars

ADD https://repo1.maven.org/maven2/org/apache/spark/spark-streaming_2.11/2.4.0/spark-streaming_2.11-2.4.0.jar \
	${SPARK_HOME}/jars

USER ${USER_NAME}

CMD $SPARK_HOME/bin/spark-submit \
	--packages "org.apache.bahir:spark-streaming-mqtt_2.11:2.4.0" \
	--conf spark.driver.extraJavaOptions="-Divy.cache.dir=/tmp -Divy.home=/tmp" \
	/pyspark/main.py
