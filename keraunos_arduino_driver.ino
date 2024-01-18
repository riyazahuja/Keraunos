//note: arduino digital pins output 5V or 0V

const int zVel = 0;
const int turnAngle = 0;
const int xVel = 0;
const int yVel = 0;

const int drone1_zVel_pin = 1;
const int drone1_turnAngle_pin = 2;
const int drone1_xVel_pin = 3;
const int drone1_yVel_pin = 4;

const int drone2_zVel_pin = 5;
const int drone2_turnAngle_pin = 6;
const int drone2_xVel_pin = 7;
const int drone2_yVel_pin = 8;

const int drone3_zVel_pin = 9;
const int drone3_turnAngle_pin = 10;
const int drone3_xVel_pin = 11;
const int drone3_yVel_pin = 12;

void sendSignal(int pin_num, int val) {
  //to go forward w joystick, need to add 1,5V, to go back need to subtract 1.5
  //joystick remains at 1.5V when not moved
  //maybe needs extra pin to specify whether positive or negative?
  
  if (val < 0) val = 0;
  else val = 1;

  //send new val
  for (int i = pin_num; i < 13; i++4) {
    digitalWrite(i, val);
  }

  delay(500);

  //need to reset button
  for (int i = pin_num; i < 13; i++4) {
    digitalWrite(i, val);
  }

}

void sendLeftJoystickSignal(int z, int turn) {
  //changing zVel
  if (z != 0) {
    if (z > 0) {
      //send voltage to go up to pin
    }

    else {
      //send voltage to go down to pin
    }
  }

  //changing turnAngle
  else if (turn != 0)
    if (turn > 0) {
      //send voltage to go up to pin
    }

    else {
      //send voltage to go down to pin
    }
}

void sendRightJoystickSignal(int x, int y) {
  //changing xVel
  if (x != 0) {
    if (x > 0) {
      //send voltage to go right to pin
    }

    else {
      //send voltage to go left to pin
    }
  }

  //changing yVel
  else if (y != 0)
    if (y > 0) {
      //send voltage to go forward to pin
    }

    else {
      //send voltage to go backwards to pin
    }
}

void setup() {
  Serial.println("Arduino Ready!");

  pinMode(drone1_zVel_pin, OUTPUT);
  pinMode(drone1_turnAngle_pin, OUTPUT);
  pinMode(drone1_xVel_pin, OUTPUT);
  pinMode(drone1_yVel_pin, OUTPUT);

  pinMode(drone2_zVel_pin, OUTPUT);
  pinMode(drone2_turnAngle_pin, OUTPUT);
  pinMode(drone2_xVel_pin, OUTPUT);
  pinMode(drone2_yVel_pin, OUTPUT);

  pinMode(drone3_zVel_pin, OUTPUT);
  pinMode(drone3_turnAngle_pin, OUTPUT);
  pinMode(drone3_xVel_pin, OUTPUT);
  pinMode(drone3_yVel_pin, OUTPUT);

}

void loop() {
  if (Serial.availiable() > 0) {
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
      Serial.println("Up");
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

    case default:
      break;
  }
}
