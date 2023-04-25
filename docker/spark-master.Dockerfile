FROM apache/spark:3.4.0

ARG SPARK_MASTER_HOST=0.0.0.0
ARG SPARK_MASTER_PORT=7077

ENV SPARK_MASTER_HOST=${SPARK_MASTER_HOST}
ENV SPARK_MASTER_PORT=${SPARK_MASTER_PORT}
ENV SPARK_NO_DAEMONIZE=true

RUN mkdir -p /opt/spark/logs && chmod a+wr /opt/spark/logs

# vvv Spark master port vvv
EXPOSE ${SPARK_MASTER_PORT}
# vvv Web UI port vvv
EXPOSE 8080

ENTRYPOINT /opt/spark/sbin/start-master.sh -h $SPARK_MASTER_HOST -p $SPARK_MASTER_PORT
