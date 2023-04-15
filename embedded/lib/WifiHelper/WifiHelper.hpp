#ifndef WIFI_HELPER_HPP
#define WIFI_HELPER_HPP

#include <WiFi.h>
#include <string>

namespace WifiHelper {
	void setup(std::string ssid, std::string password);
}

#endif//WIFI_HELPER_HPP