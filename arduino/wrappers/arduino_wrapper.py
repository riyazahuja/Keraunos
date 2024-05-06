import serial
import time
from ps4_controller import MyController


zVel = 0
turnAngle = 0
xVel = 0
yVel = 0

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=0.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.1)
    data = arduino.readline()
    return data

def main():
    controller = MyController('/dev/input/js0')
    controller.listen()

if __name__ == '__main__':
    main()
