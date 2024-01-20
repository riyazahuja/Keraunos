
#include "Drone.h";

const int zVel = 0;
const int turnAngle = 0;
const int xVel = 0;
const int yVel = 0;


// pin[0] is 1.5V zVel, pin[1] is 3V zVel
// pin[2] is 1.5V xVel, pin[3] is 3V xVel
// pin[4] is 1.5V yVel, pin[5] is 3V yVel
int pins1[6] = {2, 3, 4, 5, 6};

Drone drone1(pins1, true);

char recievedChar;
bool on;

void setup() {
  //115200 before, why?
  Serial.begin(115200);
  Serial.setTimeout(1);
  
  drone1.begin();

  on = true;

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
    
    case 'o':
      Serial.println("Up");
      drone1.up();
      break;
    case 'p':
      Serial.println("Down");
      drone1.down();
      break;

    /*
    case 'n':
      Serial.println("Turn Left");
      drone1.left();
      break;
    case 'm':
      Serial.println("Turn Right");
      drone1.right();
      break;
    */
    case 'w':
      Serial.println("Forward");
      drone1.forward();
      break; 
    case 's':
      Serial.println("Back");
      drone1.back();
      break;
    case 'a':
      Serial.println("Left");
      drone1.left();
      break;
    case 'd':
      Serial.println("Right");
      drone1.right();
      break;

    default:
      break;
  }

  recievedChar = 0;
}
