
#include "Arduino.h"
#include "Drone.h"


Drone::Drone(int pin)
{
  _pin = pin;
}

void Drone::begin()
{
  pinMode(_pin, OUTPUT);
}