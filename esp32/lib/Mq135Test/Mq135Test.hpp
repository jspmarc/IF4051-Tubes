#ifndef MQ135_TEST_HPP
#define MQ135_TEST_HPP

#include <Arduino.h>
#include <MQUnifiedsensor.h>

#define placa "ESP-32"
#define type "MQ-135"

namespace Mq135Test {
  const uint8_t analog_pin = 4;
  const uint8_t internal_led_pin = 2;
  const float voltage_resolution = 5;
  const uint8_t adc_bit_resolution = 12;
  const float ratio_clean_air = 3.6;

  void setup();
  void loop();
}

#endif//MQ135_TEST_HPP