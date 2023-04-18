#ifndef MQ135_TEST_HPP
#define MQ135_TEST_HPP

#include <Arduino.h>
#include <MQ135.h>
#include <tuple>

#ifndef MQ135_PIN
#define MQ135_PIN A0
#endif//MQ135_PIN

namespace Mq135Test {
	void setup();
	void setup();
	std::tuple<float, float> loop();
	std::tuple<float, float> loop(float temp_c, float humidity);
}

#endif//MQ135_TEST_HPP