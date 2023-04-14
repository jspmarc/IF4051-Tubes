#include <Arduino.h>

#include <MQ135.h>
#include <TimeHelper.hpp>
#include <WifiHelper.hpp>

#include <DhtTest.hpp>
#include <Mq135Test.hpp>
#include <ServoTest.hpp>

#define WIFI_SSID "tomat"
#define WIFI_PASS "23101977"

void setup() {
  Serial.begin(9600);

  analogReadResolution(10);

  // DhtTest::setup();
  // Mq135Test::setup();
  // ServoTest::setup();

  TimeHelper::setup();
  WifiHelper::setup(WIFI_SSID, WIFI_PASS);
}

void loop() {
  // Wait a few seconds between loops
  delay(1000);

  // DhtTest::loop();
  // Mq135Test::loop();
  // ServoTest::loop();

  unsigned long epoch_time = TimeHelper::get_epoch_time();
  Serial.printf("Epoch time: %ld\n", epoch_time);
}