#ifndef MQ135_TEST_HPP
#define MQ135_TEST_HPP

#include <Arduino.h>
#include <MQUnifiedsensor.h>
#include <tuple>

#define placa "ESP-32"
#define type "MQ-135"

namespace Mq135Test {
	void setup();
	std::tuple<float, float> loop(float temp_c, float humidity);
}

#endif//MQ135_TEST_HPP