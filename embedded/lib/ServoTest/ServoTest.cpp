#include "ServoTest.hpp"

Servo servo;

void ServoTest::setup() {
	servo.attach(servo_pin);
}

int16_t pos_deg = 0;      // position in degrees

void ServoTest::loop() {
	Serial.println("Servo loop start");

	if (pos_deg <= 90) {
		for (; pos_deg <= 180; pos_deg++) {
			servo.write(pos_deg);
			delay(15);
		}
		Serial.println("Servo rotated to 180 degree");
	} else {
		for (; pos_deg >= 0; pos_deg--) {
			servo.write(pos_deg);
			delay(15);
		}
		Serial.println("Servo rotated to 0 degree");
	}

	Serial.println("Servo end loop");
}