#ifndef _LIB_TURBINE_
#define _LIB_TURBINE_

#include "Arduino.h"

/*!
 *   @brief  Class that stores state and functions for interacting with turbine
 */
class Turbine {
public:
	Turbine(String zone, String id);
	//~Turbine();
	void update_state();

private:
  String serial_zone;
	String serial_id;
  int currentstate;
  int motor_pos;
};

#endif
