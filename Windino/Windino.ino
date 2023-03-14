#include <Wire.h>
#include <Adafruit_INA219.h>
#include "Serial_Bridge.h"

const String zone = "01";
const String id = "001";
Adafruit_INA219 ina219;
Serial_Bridge bridge_connection(zone, id);

int revsensorPin = 3;
int revcount = 0;
int revsensorValue = 1;

int startmillis = 0;
int currentstate;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at the value of macro SERIAL_SPEED
  Serial.begin(SERIAL_SPEED);

  if (! ina219.begin()) {
      Serial.println(" Failed to find INA219 chip ");
      while (1) { delay(10); }
    }

  if (! bridge_connection.begin()) {
      Serial.println(" Failed to connect to bridge");
      while (1) { delay(10); }
    } 

  ina219.setCalibration_16V_400mA();
  
  startmillis = millis() / 1000;
}

// the loop routine runs over and over again forever:
void loop() {
  int rev_temp = digitalRead(revsensorPin);
  if(rev_temp == 0 && rev_temp != revsensorValue)
    revcount++;
  revsensorValue = rev_temp;

// if timer >= 1s it sends data packs 
  if((millis() / 1000) - startmillis >= 1){
    float shuntvoltage = ina219.getShuntVoltage_mV();
    float busvoltage = ina219.getBusVoltage_V();
    float current_mA = ina219.getCurrent_mA();
    float loadvoltage = busvoltage + (shuntvoltage / 1000);
    float power_mW = ina219.getPower_mW();
  
    bridge_connection.print_pack(loadvoltage, "V_value_");    //voltage value V
    bridge_connection.print_pack(current_mA, "mA_value_");   //current value mA
    bridge_connection.print_pack(power_mW, "mW_value_");   //power value mW
    bridge_connection.print_pack(revcount, "R_value_");   //rev count value
    
    startmillis = millis() / 1000;    //reset timer
    revcount = 0;    //reset rev count
  }

if(Serial.available() > 0){
    char val = Serial.read();

    int futurestate;
    if(currentstate == 0 && val == 'A') futurestate = 1;
    if(currentstate == 1 && val == '1') futurestate = 2;    //acceso
    if(currentstate == 2 && val == 'S') futurestate = 3;
    if(currentstate == 3 && val == '1') futurestate = 4;    //spento
    if(currentstate == 1 && val == '2') futurestate = 5;    //acceso
    if(currentstate == 5 && val == 'S') futurestate = 6;
    if(currentstate == 6 && val == '2') futurestate = 7;    //spento

    if(currentstate != futurestate){
      if(futurestate == 2) {
        digitalWrite(13,HIGH);
      }
      if(futurestate == 4) {
        digitalWrite(13,LOW);
        futurestate = 0;
      }
      if(futurestate == 5) {
        digitalWrite(12,HIGH);
      }
      if(futurestate == 7) {
        digitalWrite(12,LOW);
        futurestate = 0;
      }
    }
    else{
      if(currentstate < 2) futurestate = 0;
      if(currentstate >= 2 && currentstate < 4) futurestate = 2;
      if(currentstate >= 5) futurestate = 5;
    }
    currentstate = futurestate;
  }

}
