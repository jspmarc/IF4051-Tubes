#ifndef INFLUX_DB_HELPER
#define INFLUX_DB_HELPER

#include <InfluxDbClient.h>
#include <InfluxDbCloud.h>
#include <string>

namespace InfluxDbHelper {
#if INSIDE_MODE==1
	static Point point("dht22");
#else//INSIDE_MODE==0
	static Point point("mq135");
#endif//INSIDE_MODE

	static InfluxDBClient client;

	void setup(
		const char *server_url,
		const char *org,
		const char *bucket,
		const char *auth_token
	);

#if INSIDE_MODE==1
	void write_data(float humidity, float temperature);
#else//INSIDE_MODE==0
	void write_data(float co2ppm);
#endif//INSIDE_MODE
}

#endif//INFLUX_DB_HELPER