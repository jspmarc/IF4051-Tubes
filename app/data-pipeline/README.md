# Data Pipeline Module
## About
Data pipeline using PySpark that listens to MQTT stream.

## How to Run
1. Start the container(s):
    - All container
        ```sh
        docker compose up -d --build
        ```

    - Specific container
        ```sh
        docker compose up -d --build <container_name>
        ```

2. Start the `pyspark`
    1. Attach to container
        ```sh
        docker exec -it pyspark bash
        ```
    2. Start the pyspark
        ```sh
        /opt/spark/bin/spark-submit --packages \
            org.apache.bahir:spark-streaming-mqtt_2.11:2.4.0 \
            main.py
        ```

3. To stop the container(s):
    - All container
        ```sh
        docker compose stop
        ```

    - Specific container
        ```sh
        docker compose stop <container_name>
        ```

## Author(s)
1. [jeremiaaxel](https://github.com/jeremiaaxel)