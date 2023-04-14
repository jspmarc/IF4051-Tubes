#include <Arduino.h>
#include <MQ135.h>

#include <DhtTest.hpp>
#include <Mq135Test.hpp>
#include <ServoTest.hpp>

void setup() {
  Serial.begin(9600);

  analogReadResolution(10);

  // DhtTest::setup();
  Mq135Test::setup();
  // ServoTest::setup();
}

void loop() {
  // Wait a few seconds between loops
  delay(1000);

  // DhtTest::loop();
  Mq135Test::loop();
  // ServoTest::loop();
}