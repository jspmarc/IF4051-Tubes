#include "MqttHelper.hpp"

void MqttHelper::setup(PubSubClient &client, MQTT_CALLBACK_SIGNATURE) {
	client.setCallback(callback);
}

void MqttHelper::reconnect(PubSubClient &client, const char *mqtt_id, const char *mqtt_user, const char *mqtt_pass) {
	while (!client.connected()) {
		Serial.println("Connecting to MQTT broker...");
		if (client.connect(mqtt_id, mqtt_user, mqtt_pass)) {
			client.subscribe(MQTT_SERVO_TOPIC);
			Serial.printf("MQTT connected and subscribed to %s\r\n", MQTT_SERVO_TOPIC);
		} else {
			Serial.printf("Failed to connect, rc=%d\r\n", client.state());
			Serial.println("Retrying in 5 secs...");
			delay(5000);
		}
	}
}

void MqttHelper::publish_dht22_data(PubSubClient &client, float humidity, float temperature, uint64_t timestamp) {
	char payload[128];
	sprintf(payload, "{\"humidity\":%.2f,\"temperature\":%.2f,\"created_timestamp\":%llu}", humidity, temperature, timestamp);
	client.publish(MQTT_DHT22_TOPIC, payload);
}

void MqttHelper::publish_mq135_data(PubSubClient &client, float co2ppm, uint64_t timestamp) {
	char payload[128];
	sprintf(payload, "{\"co2\":%.2f,\"created_timestamp\":%llu}", co2ppm, timestamp);
	client.publish(MQTT_MQ135_TOPIC, payload);
}