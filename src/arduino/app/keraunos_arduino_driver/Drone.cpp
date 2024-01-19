
#include "Arduino.h"
#include "Drone.h"

//note: arduino digital pins output 5V or 0V
Drone::Drone(int pins[], bool valid)
{
  _valid = valid;
  for(int i=0; i<4; i++){ 
    _pins[i] = pins[i];
  }
}

void Drone::begin()
{
  for(int i=0; i<4; i++){
    pinMode(_pins[i], OUTPUT);
  }
  
}

void Drone::sendSignal(int pin_num, int val) {
  //to go forward w joystick, need to add 1,5V, to go back need to subtract 1.5
  //joystick remains at 1.5V when not moved
  //maybe needs extra pin to specify whether positive or negative?
  
  if (val < 0) val = 0;
  else val = 1;

  //send new val
  digitalWrite(pin_num, val);

  delay(1000);

  //need to reset button 
  //TODO why was it ~val before? changed to zero
  digitalWrite(pin_num, 0);

}

void Drone::sendLeftJoystickSignal(int z, int turn) {
  //changing zVel
  if (z != 0) {
    sendSignal(_pins[0], z);
  }

  //changing turnAngle
  else if (turn != 0) {
    sendSignal(_pins[1], turn);
  }
}

void Drone::sendRightJoystickSignal(int x, int y) {
  //changing xVel
  if (x != 0) {
    sendSignal(_pins[2], x);
  }

  //changing yVel
  else if (y != 0) {
    sendSignal(_pins[3], y);
  }

}





