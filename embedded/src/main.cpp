#include <Arduino.h>
#include <MQ135.h>

#include <constants.hpp>
#include <MqttHelper.hpp>
#include <TimeHelper.hpp>
#include <WifiHelper.hpp>
#include <DhtTest.hpp>
#include <Mq135Test.hpp>
#include <ServoTest.hpp>

static int8_t servo_counter = 0;
static WiFiClient wifi_client;
static PubSubClient mqtt_client(MQTT_HOST, MQTT_PORT, wifi_client);

void setup() {
	Serial.begin(9600);

	DhtTest::setup();
	Mq135Test::setup();
	// ServoTest::setup();

	WifiHelper::setup(WIFI_SSID, WIFI_PASS);
	TimeHelper::setup();
	MqttHelper::setup(mqtt_client, nullptr);
}

void loop() {
	// Wait a few seconds between loops
	delay(1000);

	if (!mqtt_client.connected()) {
		MqttHelper::reconnect(mqtt_client, MQTT_ID, MQTT_USER, MQTT_PASS);
	}
	mqtt_client.loop();

	unsigned long unix_timestamp = TimeHelper::get_epoch_time();
	Serial.printf("Epoch time: %ld\n", unix_timestamp);

	auto [humidity, temperature] = DhtTest::loop();
	Serial.printf("Humidity: %.2f%% | Temperature: %.2f°C\n", humidity, temperature);
	MqttHelper::publish_dht22_data(mqtt_client, humidity, temperature, unix_timestamp);

	auto [rzero, ppm] = Mq135Test::loop(temperature, humidity);
	Serial.printf("RZero: %f\tPPM: %f\n", rzero, ppm);
	MqttHelper::publish_mq135_data(mqtt_client, ppm, unix_timestamp);

	// auto degree = ServoTest::loop(servo_counter);
	// servo_counter = servo_counter ? 0 : 2;
	// Serial.printf("Rotated to %d degree\n", degree);

	Serial.println("=================================");
}