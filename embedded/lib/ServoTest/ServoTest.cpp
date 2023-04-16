#include "ServoTest.hpp"

static Servo servo;

void ServoTest::setup() {
	servo.attach(SERVO_PIN);
}

uint16_t ServoTest::loop(uint8_t multiple) {
	if (multiple == 1) {
		servo.write(servo_45_deg);
		return 45;
	}
	
	if (multiple == 2) {
		servo.write(servo_90_deg);
		return 90;
	}

	servo.write(servo_0_deg);
	return 0;
}