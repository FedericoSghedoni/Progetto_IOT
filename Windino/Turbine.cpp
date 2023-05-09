#include "Turbine.h"
#include <Servo.h> 
#include <math.h>

/*!
  *  @brief  Instantiates a new Turbine class
  *  @param 
  */
Turbine::Turbine(String zone, String id, int motor_pos) {
  t_zone = zone;
	t_id = id;
  t_motor_pos = motor_pos;
  currentstate = 0;
  Servo myservo;  // create servo object to control a servo
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

/*!
 *  @brief  rotate turbine
 */
void Turbine::rotate(int pos) {
  int start = myservo.read();
  int dest = (pos - t_motor_pos + 360) % 360 / 2;   // 2 è il rapporto tra palo e puleggia
  for (int i = start; i != dest; i + 1 - 2 * (dest < start)) {    // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(i);              // tell servo to go to position in variable 'pos'
    delay(20);                     // waits 20ms for the servo to reach the position
  }
  return;
}
