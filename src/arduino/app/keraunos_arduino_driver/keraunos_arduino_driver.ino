
#include "Drone.h";

const int zVel = 0;
const int turnAngle = 0;
const int xVel = 0;
const int yVel = 0;

//for each drone, pin 1 is zVel, pin 2 is turnAngle, pin3 is xVel, pin4 is yVel

int pins1[4] = {2, 3, 4, 5};
int pins2[4] = {6, 7, 8, 9};
int pins3[4] = {10, 11, 12, 13};

Drone drone1(pins1, true);
Drone drone2(pins2, true);
Drone drone3(pins3, true);

char recievedChar;
bool on;

void setup() {
  //115200 before, why?
  Serial.begin(115200);
  Serial.setTimeout(1);
  
  drone1.begin();
  drone2.begin();
  drone3.begin();

  pinMode(13, OUTPUT);
  on = true;

  for (int i = 1; i < 13; i++) {
    digitalWrite(i, LOW);
  }
  
}

void loop() {

  if (Serial.available() > 0) {
    recievedChar = Serial.read();
    // say what you got:
                Serial.print("I received: ");
                Serial.println(recievedChar);
  }

  //Serial.print(recievedChar);

  switch (recievedChar)
  {
    case 'f':
      Serial.print("START");
      if(on == true){
        digitalWrite(13, LOW);
        delay(200);
        //on = false;
        digitalWrite(13, HIGH);
      }
      else{
        digitalWrite(13, HIGH);
        on = true;
      }
        

      break;
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

  recievedChar = 0;
}
