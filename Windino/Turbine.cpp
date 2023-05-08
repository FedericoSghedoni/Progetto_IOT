#include "Turbine.h" 
#include <math.h>

/*!
  *  @brief  Instantiates a new Turbine class
  *  @param 
  */
Turbine::Turbine(String zone, String id) {
  serial_zone = zone;
	serial_id = id;
  currentstate = 0;
  motor_pos = motor_pos;
}

/*!
 *  @brief  update turbine state
 */
void Turbine::update_state() {
  if(Serial.available() > 0){
    char val = Serial.read();

    int futurestate;
    if(currentstate == 0 && val == 'A') futurestate = 1;
    if(currentstate == 1 && val == '0') {
      futurestate = 0;    
      //ruota verso vento
    }
    if(currentstate == 1 && val == '1') {
      futurestate = 0;    
      //ruota dir opposta al vento
    }
    if(currentstate == 0 && val == 'L') futurestate = 2;
    if(currentstate == 2 && val == '0') {
      futurestate = 0;    
      //digitalWrite(13,LOW);
    }
    if(currentstate == 2 && val == '1') {
      futurestate = 0;    
      //digitalWrite(13,HIGH);
    }
    if(currentstate == 0 && val == 'D') futurestate = 3;
    if(currentstate == 3) {
      String direction = Serial.readString();
      Serial.print(direction);     
    }      
    currentstate = futurestate;
  }
	return;
}
