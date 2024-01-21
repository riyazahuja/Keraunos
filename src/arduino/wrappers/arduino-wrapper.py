import serial
import time
import keyboard
import json

zVel = 0
turnAngle = 0
xVel = 0
yVel = 0

arduino = serial.Serial(port='/dev/cu.usbmodem2101', baudrate=9600, timeout=0.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.1)
    data = arduino.readline()
    return data

# def main():
#     print("connected to com7.\n")

#     while True:
#         key = keyboard.read_key()

#         if key not in ['w', 'a', 's', 'd', 'o', 'p', 'n', 'm']: continue
#         else: print((write_read(key)))

def get_key_from_k(k):
    if k == "turnl":
        return 'a'
    elif k == "turnr":
        return 'd'
    elif k == "up":
        return 'o'
    elif k == "down":
        return 'p'
    elif k == "forward":
        return 'w'
    elif k == "back":
        return 's'
    return None

def main():
    print("connected to com7.\n")

    while True:
        fc={}
        try:
            with open('./../../../data.json','r') as file:
                fc = json.load(file)
        except:
            continue
        #print(fc)

        for k,v in fc['drones']['1'].items():
            if v!= 0:
                key = get_key_from_k(k)
                if key is not None:
                    print(write_read(key))            

        # if key not in ['w', 'a', 's', 'd', 'o', 'p', 'n', 'm']: continue
        # else: print((write_read(key)))

main()
