#include "WifiHelper.hpp"
#include <WiFi.h>

void WifiHelper::setup(std::string ssid, std::string password) {
	WiFi.mode(WIFI_STA);
	WiFi.begin(ssid.c_str(), password.c_str());
	Serial.print("Connecting to WiFi ..");
	while (WiFi.status() != WL_CONNECTED) {
		Serial.print('.');
		delay(1000);
	}
}