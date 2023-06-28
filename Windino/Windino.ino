#include <Wire.h>
#include <Adafruit_INA219.h>
#include "Serial_Bridge.h"
#include "Turbine.h"

//Pala 1: 01  001 180
//Pala 2: 01  002 0

Adafruit_INA219 ina219;
Turbine turbine("01", "002", 0);
Serial_Bridge bridge_connection(turbine);

int readtimer, sendtimer = 0;
float shuntvoltage = 0;
float busvoltage = 0;
float loadvoltage = 0;
float current_mA[] = {0, 0};
float loadmean[] = {0, 0};
float power_mW[] = {0, 0};
float revcount = 0;
int n = 0;

int currentstate = 0;

void send_packs(){
    bridge_connection.print_pack(loadmean[0], "V_value_");    //voltage value V
    bridge_connection.print_pack(current_mA[0], "mA_value_");   //current value mA
    bridge_connection.print_pack(power_mW[0], "mW_value_");   //power value mW
    bridge_connection.print_pack(revcount, "R_value_");   //rev count value
    loadmean[0], loadmean[1] = 0;
    current_mA[0], current_mA[1] = 0;
    power_mW[0], power_mW[1] = 0;
    revcount = 0;
    n = 0;
    sendtimer = millis() / 1000;    //reset timer
}

void online_mean(float old[], float value){
  if(value < 0)
    value = 0;
  float delta = value - old[0];
  if(delta < 0 )
    delta *= (1 / pow(n, 0.25));  
  old[0] += delta / n;
  old[1] += delta * (value - old[0]);
}

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
  
  turbine.attachRGB();
  turbine.myservo.attach(8);
  
  readtimer = millis() / 1000;
  sendtimer = millis() / 1000;
}

// the loop routine runs over and over again forever:
void loop() {
// if timer >= 1s it reads data
  if((millis() / 1000) - readtimer >= 1){
    n++;
    shuntvoltage = ina219.getShuntVoltage_mV();
    busvoltage = ina219.getBusVoltage_V();
    loadvoltage = busvoltage + (shuntvoltage / 1000);

    online_mean(loadmean, loadvoltage);
    online_mean(current_mA, ina219.getCurrent_mA());
    online_mean(power_mW, ina219.getPower_mW());
    revcount = loadmean[0] * 300;
    
    readtimer = millis() / 1000;    //reset timer
  }

 float revmax = max(loadvoltage, loadmean[0]) * 300;
  
 if((millis() / 1000) - sendtimer >= 10 && revmax > 100){
    send_packs();
  }
  if((millis() / 1000) - sendtimer >= 15 && revmax > 80){
    send_packs();
  }
  else if((millis() / 1000) - sendtimer >= 20){
    send_packs();
  }
  
  turbine.update_state();
}
