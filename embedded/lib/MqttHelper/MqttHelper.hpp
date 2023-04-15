#ifndef MQTT_HELPER_HPP
#define MQTT_HELPER_HPP

#include <PubSubClient.h>

namespace MqttHelper {
	const char *const MQTT_DHT22_TOPIC = "dht22";
	const char *const MQTT_MQ135_TOPIC = "mq135";
	const char *const MQTT_SERVO_TOPIC = "servo";

	void setup(PubSubClient &client, MQTT_CALLBACK_SIGNATURE);
	void reconnect(PubSubClient &client, const char *mqtt_id, const char *mqtt_user = nullptr, const char *mqtt_pass = nullptr);

	void publish_dht22_data(PubSubClient &client, float humidity, float temperature, uint64_t timestamp);
	void publish_mq135_data(PubSubClient &client, float co2ppm, uint64_t timestamp);
}

#endif//MQTT_HELPER_HPP