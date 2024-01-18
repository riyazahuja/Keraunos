//note: arduino digital pins output 5V or 0V


const int zVel = 0;
const int turnAngle = 0;
const int xVel = 0;
const int yVel = 0;

//for each drone, pin 1 is zVel, pin 2 is turnAngle, pin3 is xVel, pin4 is yVel
const int pins[12] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 };

void sendSignal(int pin_num, int val) {
  //to go forward w joystick, need to add 1,5V, to go back need to subtract 1.5
  //joystick remains at 1.5V when not moved
  //maybe needs extra pin to specify whether positive or negative?
  
  if (val < 0) val = 0;
  else val = 1;

  //send new val
  for (int i = pin_num; i < 13; i= i+4) {
    digitalWrite(i, val);
  }

  delay(500);

  //need to reset button
  for (int i = pin_num; i < 13; i = i+4) {
    digitalWrite(i, val);
  }

}

void sendLeftJoystickSignal(int z, int turn) {
  //changing zVel
  if (z != 0) {
    sendSignal(1, z);
  }

  //changing turnAngle
  else if (turn != 0) {
    sendSignal(2, turn);
  }
}

void sendRightJoystickSignal(int x, int y) {
  //changing xVel
  if (x != 0) {
    sendSignal(3, x);
  }

  //changing yVel
  else if (y != 0) {
    sendSignal(4, y);
  }

}

void setup() {
  Serial.println("Arduino Ready!");

  for (int i = 0; i < 12; i++)
  {
    pinMode(pins[i], OUTPUT);
  }

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
      sendLeftJoystickSignal(1, 0);
      break;
    case 'p':
      Serial.println("Down");
      sendLeftJoystickSignal(-1, 0);
      break;

    case 'n':
      Serial.println("Turn Left");
      sendLeftJoystickSignal(0, -1);
      break;
    case 'm':
      Serial.println("Turn Right");
      sendLeftJoystickSignal(0, 1);
      break;

    case 'w':
      Serial.println("Forward");
      sendRightJoystickSignal(0, 1);
      break; 
    case 'a':
      Serial.println("Left");
      sendRightJoystickSignal(-1, 0);
      break;
    case 's':
      Serial.println("Back");
      sendRightJoystickSignal(0, -1);
      break;
    case 'd':
      Serial.println("Right");
      sendRightJoystickSignal(1, 0);
      break;

    default:
      break;
  }
}
