# IF4051 Final Project 
Air quality is an important aspect of a room. It affects the health, comfort, and productivity of the occupants. This paper presents an Internet-of-Things based system that can be used to monitor the air quality of a room and the outside air, and control the door/window of the room in hope of achieving a better air quality. The system will be able to monitor the air quality of a room, with temperature and humidity as the indicators, using DHT22 sensor; and the outside, with carbon dioxide (CO<sub>2</sub>) ppm as the indicator, using MQ135 sensor; and ESP32 as the microprocessor. The system also utilizes Time Series KMeans (TSKM) to determine the quality of the indicators, to decide whether to open or close the door.

<strong> TL;DR\
IoT System that make a room's air condition better by controlling the door(s)/window(s). \
Utilizes machine learning (TimeSeriesKMeans) to determine the door(s)/window(s)'s open/close. \
Indicator(s):
1. Inside: Temperature and Humidity, uses DHT22 sensor
2. Outside: Carbon dioxide, uses MQ135 sensor   
</strong>

## Features
### 1. Home View
System control: change AI/manual mode, remote control.
  > :warning: Alarm(s) feature is not developed.
<img src="paper/src/resources/webapp-home-view.png" width="500" height="auto">

### 2. Stats View
See realtime statistic of air condition. \
<img src="paper/src/resources/webapp-stats-view.png" width="500" height="auto">

### 3. Alerts View
See alerts from AI of the air condition. \
<img src="paper/src/resources/webapp-alerts-view.png" width="500" height="auto">

## Technologies Used:
1. Web Application:
    1. Frontend: Vue 3, TypeScript, Vite; TailwindCSS
    2. Backend: FastAPI, Python 3; Redis; InfluxDB
    3. Protocol: REST API; WebSocket
2. Data Pipeline/Messaging Queue: MQTT; Kafka; PySpark
3. Embedded:
    1. Components: ESP32; MQ135; DHT22
    2. Code: C++; platformio
5. Machine Learning: TimeSeriesKMeans (tslearn; Python 3)
6. Containerization: Docker

## Distribution of Tasks
| Name | Student ID | Tasks |
|---|---|---|
| Josep Marcello | 13519164 | 1. Define system architecture<br>2. Calibrate sensors<br>3. Setup application and ESP32 boilerplate code<br>4. Setup infrastructure (including MQTT, InfluxDB, Telegraf, and Redis)<br>5. Connect ESP32 with time server<br>6. Develop ESP32 so it's able to control actuator and send sensor data at the same time<br>7. Establish connection between ESP32 and application through MQTT<br>8. Develop servo toggle feature (back-end)<br>9. Develop state manager for application back-end<br>10. Develop e-email notification and API to get all sent notifications<br>11. Develop simple app password system<br>12. Develop (almost realtime) statistics feature<br>13. Develop realtime data feature<br>14. Integrate ML model to web app<br>15. Setup docker for infrastructure and application<br>16. Code review<br>17. Server donation |
| Jeremia Axel B. | 13519188 | 1. Define early data pipeline architecture<br>2. Develop MQTT-PySpark for data aggregation<br>3. Develop mode toggle feature<br>4. Develop servo toggle feature (front-end)<br>5. Develop websocket to publish current state to front-end clients<br>6. Implement and train ML model<br>7. Save and use ML model in application's back-end<br>8. Initiate paper template (with sliced components)<br>9. Setup docker for data-pipeline and initial docker-compose<br>10. Create Google Slides for progress report<br>11. Code review |
| Jeane Mikha E. | 13519116 | 1. Determine ML algorithm to use<br>2. Design wireframe for web app's UI/UX<br>3. Enhance UI/UX of the web app<br>4. Develop alerts page<br>5. Edit demo video<br>6. Create poster |

## Diagram(s)
1. IoT Diagram \
    <img src="paper/src/resources/iot-diagram.png" width="500" height="auto">
2. Deployment Diagram \
    <img src="paper/src/resources/deployment-diagram.png" width="500" height="auto">
