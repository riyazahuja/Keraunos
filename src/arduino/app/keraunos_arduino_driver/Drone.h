
/*
  Drone library for control functions
*/
#ifndef Drone_h
#define Drone_h
#include <Arduino.h>

class Drone
{

  public:
    Drone(int pin);
    void begin();
    void dot();
    void dash();
  private:
    int _pin;

};

#endif