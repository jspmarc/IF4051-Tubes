#include "ServoTest.hpp"

Servo servo;

void ServoTest::setup() {
	servo.attach(servo_pin);
}

uint16_t ServoTest::loop(int8_t counter) {
	if (counter == 1) {
		servo.write(servo_45_deg);
		return 45;
	}
	
	if (counter == 2) {
		servo.write(servo_90_deg);
		return 90;
	}

	servo.write(servo_0_deg);
	return 0;
}