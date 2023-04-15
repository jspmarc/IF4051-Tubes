#include <Arduino.h>
#include <time.h>
#include "TimeHelper.hpp"

void TimeHelper::setup() {
	configTime(0, 0, NTP_SERVER);
}

uint64_t TimeHelper::get_epoch_time() {
	time_t now;
	struct tm timeinfo;
	if (!getLocalTime(&timeinfo)) {
		return 0 ;
	}
	time(&now);
	return now;
}