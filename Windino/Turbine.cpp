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
  RPin = 11;
  GPin = 10;
  BPin = 9;
  Servo myservo;  // create servo object to control a servo
  dir;
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
      rotate(dir);
    }
    if(currentstate == 1 && val == '1') {
      futurestate = 0;
      setRGB(RED);    
      rotate(dir+180);
    }
    if(currentstate == 0 && val == 'L') futurestate = 2;
    if(currentstate == 2 && val == '0') {
      futurestate = 0;    
      setRGB(GREEN);
    }
    if(currentstate == 2 && val == '1') {
      futurestate = 0;    
      setRGB(RED);
    }
    if(currentstate == 0 && val == 'D') futurestate = 3;
    if(currentstate == 3) {
      String direction = Serial.readString();
      Serial.print(direction);
      dir = direction.toInt();
      rotate(dir);
      futurestate = 0;    
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
  for (int i = start; i != dest; i += 1 - 2 * (dest < start)) {    // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(i);              // tell servo to go to position in variable 'pos'
    delay(20);                     // waits 20ms for the servo to reach the position
  }
  return;
}

/*!
 *  @brief  attach RGB led
 */
void Turbine::attachRGB() {
  pinMode(RPin, OUTPUT);
  pinMode(GPin, OUTPUT);
  pinMode(BPin, OUTPUT);
  setRGB(GREEN);
}

/*!
 *  @brief  set RGB color
 */
void Turbine::setRGB(Color color) {
  switch (color){
    case OFF:
      analogWrite(RPin, 0);
      analogWrite(GPin, 0);
      analogWrite(BPin, 0);
      break;
    case RED: 
      analogWrite(RPin, 255);
      analogWrite(GPin, 0);
      analogWrite(BPin, 0);
      break;
    case GREEN: 
      analogWrite(RPin, 0);
      analogWrite(GPin, 255);
      analogWrite(BPin, 0);
      break;
    case BLUE: 
      analogWrite(RPin, 0);
      analogWrite(GPin, 0);
      analogWrite(BPin, 255);
      break;
    case PURPLE: 
      analogWrite(RPin, 128);
      analogWrite(GPin, 0);
      analogWrite(BPin, 128);
      break;
    case YELLOW: 
      analogWrite(RPin, 237);
      analogWrite(GPin, 109);
      analogWrite(BPin, 0);
      break;
    default: break;
  }
}
