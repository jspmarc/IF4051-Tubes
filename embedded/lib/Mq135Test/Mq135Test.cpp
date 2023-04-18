#include "Mq135Test.hpp"
#include "MQ135.h"

MQ135 mq135(MQ135_PIN);

void Mq135Test::setup() {
}

std::tuple<float, float> Mq135Test::loop() {
	float resistance = mq135.getResistance();
	float rzero = mq135.getRZero(resistance);
	float ppm = mq135.getPPM(resistance);

	return std::make_tuple(rzero, ppm);
}

std::tuple<float, float> Mq135Test::loop(float temp_c, float humidity) {
	float resistance = mq135.getCorrectedResistance(temp_c, humidity);
	float rzero = mq135.getRZero(resistance);
	float ppm = mq135.getPPM(resistance);

	return std::make_tuple(rzero, ppm);
}