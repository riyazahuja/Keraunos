
#include "Drone.h";

const int zVel = 0;
const int turnAngle = 0;
const int xVel = 0;
const int yVel = 0;

//for each drone, pin 1 is zVel, pin 2 is turnAngle, pin3 is xVel, pin4 is yVel

int pins1[4] = {1, 2, 3, 4};
int pins2[4] = {5, 6, 7, 8};
int pins3[4] = {9, 10, 11, 12};

Drone drone1(pins1, true);
Drone drone2(pins2, true);
Drone drone3(pins3, true);


void setup() {
  Serial.println("Arduino Ready!");
  
  drone1.begin();
  drone2.begin();
  drone3.begin();

}

void loop() {
  char recievedChar = '1';

  if (Serial.available() > 0) {
    recievedChar = Serial.read();
  }

  switch (recievedChar)
  {
    case 'o':
      Serial.println("Up");
      drone1.sendLeftJoystickSignal(1, 0);
      break;
    case 'p':
      Serial.println("Down");
      drone1.sendLeftJoystickSignal(-1, 0);
      break;

    case 'n':
      Serial.println("Turn Left");
      drone1.sendLeftJoystickSignal(0, -1);
      break;
    case 'm':
      Serial.println("Turn Right");
      drone1.sendLeftJoystickSignal(0, 1);
      break;

    case 'w':
      Serial.println("Forward");
      drone1.sendRightJoystickSignal(0, 1);
      break; 
    case 'a':
      Serial.println("Left");
      drone1.sendRightJoystickSignal(-1, 0);
      break;
    case 's':
      Serial.println("Back");
      drone1.sendRightJoystickSignal(0, -1);
      break;
    case 'd':
      Serial.println("Right");
      drone1.sendRightJoystickSignal(1, 0);
      break;

    default:
      break;
  }
}
