#ifndef TIME_HELPER_HPP
#define TIME_HELPER_HPP

#define NTP_SERVER "pool.ntp.org"

namespace TimeHelper {
	void setup();
	unsigned long get_epoch_time();
}

#endif//TIME_HELPER_HPP