import serial
import time
import keyboard

zVel = 0
turnAngle = 0
xVel = 0
yVel = 0

arduino = serial.Serial(port='COM7', baudrate=9600, timeout=0.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.1)
    data = arduino.readline()
    return data

def main():
    print("connected to com7.\n")

    while True:
        key = keyboard.read_key()

        if key not in ['w', 'a', 's', 'd', 'o', 'p', 'n', 'm']: continue
        else: print((write_read(key)))

main()
