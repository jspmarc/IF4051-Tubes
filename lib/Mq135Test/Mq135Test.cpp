#include "Mq135Test.hpp"

MQUnifiedsensor mq135(
  placa,
  Mq135Test::voltage_resolution,
  Mq135Test::adc_bit_resolution,
  Mq135Test::analog_pin,
  type
);

void Mq135Test::setup() {
  Serial.begin(9600); // sets the serial port to 9600

  mq135.init();
  mq135.setRegressionMethod(1); //_PPM =  a*ratio^b
  mq135.setA(110.47);
  mq135.setB(-2.862);

  // mq135.setA(110.47); MQ135.setB(-2.862);
  // co2 = mq135.readSensor();

  // mq135.setA(605.18); MQ135.setB(-3.937);
  // double co = mq135.readSensor();

  // mq135.setA(77.255); MQ135.setB(-3.18);
  // double alcohol = mq135.readSensor();

  // mq135.setA(44.947); MQ135.setB(-3.445);
  // double toluene = mq135.readSensor();

  // mq135.setA(102.2 ); MQ135.setB(-2.473);
  // double nh4 = mq135.readSensor();

  // mq135.setA(34.668); MQ135.setB(-3.369);
  // double acetone = mq135.readSensor();

  Serial.print("Calibrating MQ135 sensor, please wait.");
  float calcR0 = 0;
  for(uint8_t i = 1; i <= 10; i++) {
      mq135.update(); // Update data, the arduino will be read the voltage on the analog pin
      calcR0 += mq135.calibrate(Mq135Test::ratio_clean_air);
      Serial.print(".");
  }
  mq135.setR0(calcR0 / 10);
  Serial.println("  done!");

  if (isinf(calcR0)) {
    Serial.println("Warning: Conection issue found, R0 is infite (Open circuit detected) please check your wiring and supply");
    for (;;);
  }

  if (calcR0 == 0) {
    Serial.println("Warning: Conection issue found, R0 is zero (Analog pin with short circuit to ground) please check your wiring and supply");
    for(;;);
  }

  // mq135.serialDebug(true);
}

void Mq135Test::loop() {
  mq135.update();
  double co2 = mq135.readSensor();
  Serial.print("CO2 PPM: ");
  Serial.println(co2);
  // mq135.serialDebug();
}