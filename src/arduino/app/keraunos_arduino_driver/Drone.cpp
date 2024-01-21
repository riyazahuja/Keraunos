
#include "Arduino.h"
#include "Drone.h"

//note: arduino digital pins output 5V or 0V

// pin[0] is 1.5V zVel, pin[1] is 3V zVel
// pin[2] is 1.5V xVel, pin[3] is 3V xVel
// pin[4] is 1.5V yVel, pin[5] is 3V yVel
Drone::Drone(int pins[], bool valid)
{
  _valid = valid;
  for(int i=0; i<6; i++){ 
    _pins[i] = pins[i];
  }
}

void Drone::begin()
{
  for(int i=0; i<6; i++){
    pinMode(_pins[i], OUTPUT);
  }

  
  //neutral joystick position is 1.5V
  digitalWrite(_pins[0], HIGH);

  digitalWrite(_pins[2], HIGH);
  digitalWrite(_pins[4], HIGH);

  //digitalWrite(_pins[1], HIGH);
  //digitalWrite(_pins[3], HIGH);
  //digitalWrite(_pins[5], HIGH);


}

void Drone::up(){

  //up is 3V zVel joystick, small nudge upwards
  //adjust delay for shorter nudge upwards
  digitalWrite(_pins[1], HIGH);
  delay(50);
  digitalWrite(_pins[1], LOW);

  //back to neutral joystick position, sanity check
  digitalWrite(_pins[0], HIGH);

}

void Drone::down(){

  //down is 0V zVel joystick, small nudge down
  //adjust delay for shorter nudge down
  //both neutral needs to be pulled low
  digitalWrite(_pins[0], LOW);
  digitalWrite(_pins[1], LOW);
  delay(70);
  //back to neutral joystick position
  digitalWrite(_pins[0], HIGH);
  
}

void Drone::forward(){

  //forward is 3V yVel joystick, small nudge up
  //adjust delay for shorter nudge 
  digitalWrite(_pins[3], HIGH);
  delay(100);
  digitalWrite(_pins[3], LOW);

  //back to neutral joystick position sanity check
  digitalWrite(_pins[2], HIGH);
  
}

void Drone::back(){

  //back is 0V yVel joystick, small nudge down
  //adjust delay for shorter nudge down
  //both neutral needs to be pulled low
  digitalWrite(_pins[2], LOW);
  digitalWrite(_pins[3], LOW);
  delay(120);
  //back to neutral joystick position
  digitalWrite(_pins[2], HIGH);
}


void Drone::left(){

  //left is 0V xVel joystick, small nudge down
  //adjust delay for shorter nudge down
  //both neutral needs to be pulled low
  digitalWrite(_pins[4], LOW);
  digitalWrite(_pins[5], LOW);
  delay(70);
  //back to neutral joystick position
  digitalWrite(_pins[4], HIGH);
}

void Drone::right(){

  //right is 3V xVel joystick, small nudge up
  //adjust delay for shorter nudge 
  digitalWrite(_pins[5], HIGH);
  delay(70);
  digitalWrite(_pins[5], LOW);

  //back to neutral joystick position sanity check
  digitalWrite(_pins[4], HIGH);

}

