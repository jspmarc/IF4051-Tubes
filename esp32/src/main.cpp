#include <Arduino.h>
#include <DhtTest.hpp>
#include <Mq135Test.hpp>
#include <ServoTest.hpp>

void setup() {
  delay(2000);

  Serial.begin(9600);

  DhtTest::setup();
  Mq135Test::setup();
  // ServoTest::setup();
}

void loop() {
  // Wait a few seconds between loops
  delay(500);

  DhtTest::loop();
  Mq135Test::loop();
  // ServoTest::loop();
}