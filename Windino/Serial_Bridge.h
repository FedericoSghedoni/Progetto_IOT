#ifndef _LIB_SERIAL_BRIDGE_
#define _LIB_SERIAL_BRIDGE_

#include "Arduino.h"
#include "Turbine.h" 

#define SERIAL_SPEED 9600
#define SOL '\xff'
#define EOL '\xfe'

/*!
 *   @brief  Class that stores state and functions for interacting with bridge
 */
class Serial_Bridge {
public:
	Serial_Bridge(Turbine turbine);
	//~Serial_Bridge();
	bool begin();
	void print_pack(float value, String label);

private:
  String serial_zone;
  String serial_id;
};

#endif
