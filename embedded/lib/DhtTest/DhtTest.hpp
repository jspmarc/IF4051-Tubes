#ifndef DHT_TEST_HPP
#define DHT_TEST_HPP

#include <DHT.h>
#include <tuple>

#define DHTTYPE DHT22
#ifndef DHT_PIN
/// Feather HUZZAH ESP8266 note: use pins 3, 4, 5, 12, 13 or 14 --
/// Pin 15 can work but DHT must be disconnected during program upload.
#define DHT_PIN 23
#endif//DHT_PIN

namespace DhtTest {
	void setup();
	std::tuple<float, float> loop();
}

#endif//DHT_TEST_HPP