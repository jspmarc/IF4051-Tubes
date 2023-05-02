FROM node:20-alpine3.16 AS build-fe

ARG BE_URN=localhost:8080

RUN npm i -g pnpm

RUN mkdir -p /app/be/src
COPY ./app/fe/ /app/fe/

WORKDIR /app/fe

ENV VITE_BACKEND_URN=${BE_URN}

RUN pnpm install --frozen-lockfile

RUN pnpm build

FROM python:3.11.3-alpine3.16

COPY ./app/be/ /app/be
COPY ./common-python /common-python

WORKDIR /app/be

RUN pip3 install --no-cache-dir -r requirements.txt
COPY --from=build-fe /app/be/src/public/ /app/be/src/public/

EXPOSE 8080

USER 1000

WORKDIR /app/be/src

ENV API_TOKEN=
ENV MQTT_HOST=mosquitto
ENV MQTT_PORT=1883
ENV MQTT_USER=
ENV MQTT_PASS=
ENV DB_URI=http://influxdb:8086
ENV DB_TOKEN=asd
ENV DB_ORG=asd
ENV DB_BUCKET=asd
ENV KAFKA_BOOTSTRAP_SERVER=kafka:29092
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV REDIS_PASSWORD=

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
