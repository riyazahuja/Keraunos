
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
    void up();
    void down();
    void forward();
    void back();
    void left();
    void right();

  private:
    void sendSignal(int pin_num, int val);
    bool _valid;
    int _pins [6];
    

};

#endif