
/*
  Drone library for control functions
*/
#ifndef Drone_h
#define Drone_h
#include <Arduino.h>

class Drone
{

  public:
    Drone(int pins[], bool valid);
    void begin();
    void sendLeftJoystickSignal(int z, int turn);
    void sendRightJoystickSignal(int x, int y);

  private:
    void sendSignal(int pin_num, int val);
    bool _valid;
    int _pins [4];
    

};

#endif