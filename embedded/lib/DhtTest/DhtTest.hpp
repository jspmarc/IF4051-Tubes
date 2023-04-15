#ifndef DHT_TEST_HPP
#define DHT_TEST_HPP

#include <DHT.h>
#include <tuple>

#define DHTTYPE DHT22

namespace DhtTest {
	const uint8_t DHT_PIN = 23;
	// Feather HUZZAH ESP8266 note: use pins 3, 4, 5, 12, 13 or 14 --
	// Pin 15 can work but DHT must be disconnected during program upload.

	void setup();
	std::tuple<float, float> loop();
}

#endif//DHT_TEST_HPP