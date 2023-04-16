#ifndef SERVO_TEST_HPP
#define SERVO_TEST_HPP

#include <ESP32Servo.h>

#ifndef SERVO_PIN
/// These are all GPIO pins on the ESP32
/// Recommended pins include 2,4,12-19,21-23,25-27,32-33
/// for the ESP32-S2 the GPIO pins are 1-21,26,33-42
#define SERVO_PIN 2
#endif//SERVO_PIN

namespace ServoTest {
	const uint8_t servo_0_deg = 18;
	const uint8_t servo_45_deg = 64;
	const uint8_t servo_90_deg = 110;

	void setup();
	/// @brief Degree is multiple * 45, with max multiple = 2
	/// @param multiple multiple of 45 
	/// @return the degree of the servo motor
	uint16_t loop(uint8_t multiple);
}

#endif//SERVO_TEST_HPP