#include "Mq135Test.hpp"
#include "MQ135.h"

MQ135 mq135 = MQ135(4);

void Mq135Test::setup() {
}

void Mq135Test::loop() {
  float rzero = mq135.getRZero();
  float ppm = mq135.getPPM();
  Serial.printf("rzero: %f\tppm: %f\n", rzero, ppm);
}