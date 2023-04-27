#ifndef CONSTANTS_HPP
#define CONSTANTS_HPP

#include <Arduino.h>

const char *const WIFI_SSID = "tomat";
const char *const WIFI_PASS = "23101977";

const IPAddress MQTT_HOST(103,176,78,158);
const uint16_t MQTT_PORT = 1883;
#ifndef MQTT_ID
#define MQTT_ID "esp32"
#endif//MQTT_ID
const char *const MQTT_USER = "IF4051_mqtt";
const char *const MQTT_PASS = "kerja-lembur";

#endif//CONSTANTS_HPP