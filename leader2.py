import numpy as np
import cv2
import mss
import pywinctl as pw
from datetime import datetime
import json
from math import exp, ceil
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
def get_webcam():
    webcam = cv2.VideoCapture(1) 
    _, imageFrame = webcam.read() 
    return imageFrame

def get_target_region(width,height, c0,c1):
    x0,y0 = c0
    x1,y1 = c1

    w = (x1-x0)*width
    h = (y1-y0)*height

    x = x0*width
    y=y0*height

    return (x,y,w,h)



def capture_app_window(drone_id, app_title = 'DE FPV'):


    # Define the bounding box of the window

    webcam = cv2.VideoCapture(1) 

    width = int(webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    target_region = get_target_region(width, height, (0.25,0.25), (0.75,0.75))

    while True:
        _, frame = webcam.read() 


        




        # Inference
        results = model(frame)

        # Results
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        n = len(labels)
        for i in range(n):
            row = cord[i]
            x1, y1, x2, y2 = int(row[0]*frame.shape[1]), int(row[1]*frame.shape[0]), int(row[2]*frame.shape[1]), int(row[3]*frame.shape[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = results.names[int(labels[i])]
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow("YOLOv5 Object Detection", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        
        a, b, c, d = target_region
        cv2.rectangle(frame, (int(a), int(b)), (int(a + c), int(b + d)), (0, 255, 0), 2)
        cv2.putText(frame, "Target", (int(a), int(b)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                    (0, 255,0))  
        

        data_out = calculateCommands((x1,y1,x2-x1,y2-y1),drone_id, target_region,(width,height))
        print(data_out['drones'][drone_id])
        export(data_out,'data.json')




        # Program Termination 
        cv2.imshow("Multiple Color Detection in Real-Time", frame) 
        if cv2.waitKey(10) & 0xFF == ord('q'): 
            cv2.destroyAllWindows() 
            break



#dropoff function:
#f(x) = -100e^{-0.1*x}+100
def plateau_and_round(x):
    return ceil(-100 * exp(-0.1 * x)+100)


def calculateCommands(actual_region, drone_id, target_region, window):
    x,y,w,h = actual_region
    x0,y0,w0,h0 = target_region
    role = 'LEADER' if drone_id == 1 else 'FOLLOWER'

    area = w*h
    area0 = w0*h0

    ww, wh= window
    warea = ww*wh

    turnl=turnr=up=down=forward=back = 0
    AREA_GRAN = 10
    
    area = AREA_GRAN*area

    if area < area0:
        forward = (area0-area)/warea* 100
    elif area > area0:
        back = (area-area0)/warea* 100
    
    if x<x0:
        turnr = (x0-x)/ww * 100
    elif x>x0+w0:
        turnl = (x-x0-w)/ww* 100

    if y<y0:
        up = (y0-y)/wh* 100
    elif y>y0+h0:
        down = (y-y0-h)/wh* 100

    

    data = {
        'drones': {
            drone_id : {
                'time': datetime.now().isoformat(),
                'role': role,
                'turnl': plateau_and_round(turnl),
                'turnr': plateau_and_round(turnr),
                'up': plateau_and_round(up),
                'down': plateau_and_round(down),
                'forward': plateau_and_round(forward),
                'back': plateau_and_round(back)
            }
        }
    }

    

    return data


def export(data,path):
    try:
        fc = {}
        try:
            with open(path, 'r') as file:
                fc = json.load(file)
        except:
            pass
        
        with open(path,'w') as file:
            if 'drones' not in fc.keys():
                fc['drones']={}
            for k,v in data.items():
                fc['drones'][k]=v
            
            json.dump(fc, file, indent=4)
    except Exception as e:
        print(f"An error occurred: {e}")

    




def list_window_titles():
    windows = pw.getAllTitles()
    return windows

titles = list_window_titles()
for title in titles:
    print(title)


capture_app_window(1, "GitHub Desktop")