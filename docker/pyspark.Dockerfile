FROM apache/spark-py:v3.4.0

#ADD http://search.maven.org/remotecontent?filepath=org/apache/bahir/spark-streaming-mqtt_2.11/2.4.0/spark-streaming-mqtt_2.11-2.4.0.jar $SPARK_HOME/work-dir/spark-streaming-mqtt_2.12-2.4.0.jar
#CMD $SPARK_HOME/bin/spark-submit --jars "spark-streaming-mqtt_2.12-2.4.0.jar" --conf spark.driver.extraJavaOptions="-Divy.cache.dir=/tmp -Divy.home=/tmp" /pyspark/main.py

CMD $SPARK_HOME/bin/spark-submit --packages "org.apache.bahir:spark-streaming-mqtt_2.11:2.4.0" --conf spark.driver.extraJavaOptions="-Divy.cache.dir=/tmp -Divy.home=/tmp" /pyspark/main.py
