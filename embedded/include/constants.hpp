#ifndef CONSTANTS_HPP
#define CONSTANTS_HPP

#include <Arduino.h>

#ifndef WIFI_SSID
#define WIFI_SSID "ssid";
#endif//WIFI_SSID
#ifndef WIFI_PASS
#define WIFI_PASS "password";
#endif//WIFI_PASS

const IPAddress MQTT_HOST(103,176,78,158);
const uint16_t MQTT_PORT = 1883;
const char *const MQTT_ID = "esp32";
const char *const MQTT_USER = "IF4051_mqtt";
const char *const MQTT_PASS = "kerja-lembur";

#endif//CONSTANTS_HPP