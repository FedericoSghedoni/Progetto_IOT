#ifndef _LIB_TURBINE_
#define _LIB_TURBINE_

#include "Arduino.h"
#include <Servo.h> 

/*!
 *   @brief  Class that stores state and functions for interacting with turbine
 */
class Turbine {
public:
	Turbine(String zone, String id, int motor_pos);
	//~Turbine();
  String zone;
  String id;
  Servo myservo;
	void update_state();
  void rotate(int pos);

private:
  int currentstate;
  int motor_pos;
};

#endif
