#include "Serial_Bridge.h" 
#include <math.h>

/*!
  *  @brief  Instantiates a new Serial_Bridge class
  *  @param 
  */
Serial_Bridge::Serial_Bridge(String zone, String id) {
  serial_zone = zone;
	serial_id = id;
}

/*!
 *  @brief  Sets up the connection to the bridge
 *  @return true: success false: Failed to start 
 */
bool Serial_Bridge::begin() {
	while (1) {
		if (Serial.available() > 0) {
      char msg = Serial.read();
			if (msg == SOL) {
				Serial.print(EOL); //connessione al bridge
        int zone_len = serial_zone.length();
        Serial.print(zone_len);
        Serial.print(serial_zone);
        Serial.print(serial_id);
				return true;
			}
			else
				return false;
		}
	}
}

/*!
 *  @brief  send data package
 */
void Serial_Bridge::print_pack(float value, String label) {
	int val = value * 100;
	int pack_size = int(log10(val)) + 1;
	//String topic = serial_zone + "/" + serial_id + "/" + label;   //add id to label

	Serial.print(SOL);
	Serial.print(pack_size);
	Serial.print(val);
	Serial.print(label);
	Serial.print(EOL);
	return;
}
