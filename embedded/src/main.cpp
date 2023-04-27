#include <Arduino.h>
#include <cmath>
#include <HTTPClient.h>
#include <memory>
#include <MQ135.h>

#include <constants.hpp>
#include <MqttHelper.hpp>
#include <TimeHelper.hpp>
#include <WifiHelper.hpp>
#include <DhtTest.hpp>
#include <Mq135Test.hpp>
#include <ServoTest.hpp>

#ifndef INSIDE_MODE
#define INSIDE_MODE 1
#endif//INSIDE_MODE

static WiFiClient wifi_client;
static PubSubClient mqtt_client(MQTT_HOST, MQTT_PORT, wifi_client);

static TaskHandle_t main_task_handle;
void main_task(void *params);

#if INSIDE_MODE==1
void servo_task(void *params);
void servo_callback(char *topic, uint8_t *payload, unsigned int length);

static std::shared_ptr<uint8_t> servo_multiple(nullptr);
static TaskHandle_t servo_task_handle;
#endif//INSIDE_MODE

void setup() {
	Serial.begin(115200);

	DhtTest::setup();
	Mq135Test::setup();
	ServoTest::setup();

	WifiHelper::setup(WIFI_SSID, WIFI_PASS);
	TimeHelper::setup();

#if INSIDE_MODE==0
	MqttHelper::setup(mqtt_client, nullptr);
#else//INSIDE_MODE==1
	MqttHelper::setup(mqtt_client, servo_callback);

	xTaskCreatePinnedToCore(servo_task, "Servo task", 5000, nullptr, 1, &servo_task_handle, 1);
#endif//INSIDE_MODE
	xTaskCreatePinnedToCore(main_task, "Main task", 5000, nullptr, 1, &main_task_handle, 0);
}

void loop() {}
void main_task(void *params) {
	for (;;) {
		// Wait a few seconds between loops
		delay(1000);

		while (!mqtt_client.connected()) {
			MqttHelper::reconnect(mqtt_client, MQTT_ID, MQTT_USER, MQTT_PASS);
		}
		mqtt_client.loop();

		auto unix_timestamp = TimeHelper::get_epoch_time();
		Serial.printf("Epoch time: %llu\n", unix_timestamp);

#if INSIDE_MODE==1
		auto [humidity, temperature] = DhtTest::loop();
		if (isnan(humidity) || isnan(temperature)) {
			continue;
		}
		Serial.printf("Humidity: %.2f%% | Temperature: %.2f°C\n", humidity, temperature);
		MqttHelper::publish_dht22_data(mqtt_client, humidity, temperature, unix_timestamp);
#else//INSIDE_MODE==0
		auto [rzero, ppm] = Mq135Test::loop();
		if (isnan(rzero) || isnan(ppm)) {
			continue;
		}
		Serial.printf("RZero: %f\tPPM: %f\n", rzero, ppm);
		MqttHelper::publish_mq135_data(mqtt_client, ppm, unix_timestamp);
#endif//INSIDE_MODE
		Serial.println("=================================");
	}
}

#if INSIDE_MODE==1
void servo_task(void *params) {
	for (;;) {
		delay(100);

		// the pointer is null
		if (!servo_multiple) {
			continue;
		}

		auto degree = ServoTest::loop(*servo_multiple);
		servo_multiple.reset();
		Serial.printf("Rotated servo to %d degree\n", degree);
	}
}

void servo_callback(char *topic, uint8_t *payload, unsigned int length) {
	if (strcmp(topic, MqttHelper::MQTT_SERVO_TOPIC) != 0 || length != 1) {
		return;
	}

	uint8_t counter = payload[0] - 48;
	if (counter >= 3) {
		return;
	}

	servo_multiple.reset(new uint8_t(counter));
}
#endif//INSIDE_MODE==1