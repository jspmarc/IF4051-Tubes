#include "InfluxDbHelper.hpp"

void InfluxDbHelper::setup(
	const char *server_url,
	const char *org,
	const char *bucket,
	const char *auth_token
) {
	client.setConnectionParams(server_url, org, bucket, auth_token);
	if (!client.validateConnection()) {
		Serial.print("Can't connect to InfluxDB: ");
		Serial.println(client.getLastErrorMessage());
	} else {
		Serial.print("Connected to InfluxDB");
	}
}

#if INSIDE_MODE==1
void InfluxDbHelper::write_data(float humidity, float temperature) {
	point.clearFields();
	point.addField("humidity", humidity);
	point.addField("temperature", temperature);
	if (!client.writePoint(point)) {
		Serial.print("Can't write point InfluxDB: ");
		Serial.println(client.getLastErrorMessage());
	}
}
#else//INSIDE_MODE==0
void InfluxDbHelper::write_data(float co2ppm) {
	point.clearFields();
	point.addField("co2", co2ppm);
	if (!client.writePoint(point)) {
		Serial.print("Can't write point to InfluxDB: ");
		Serial.println(client.getLastErrorMessage());
	}
}
#endif//INSIDE_MODE