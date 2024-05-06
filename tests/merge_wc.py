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
        imageFrame = frame

        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
        #imageFrame=hsvFrame


        # Set range for red color and define mask
        red_lower = np.array([136, 87, 111], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

        
        # Morphological Transform, Dilation 
        # for each color and bitwise_and operator 
        # between imageFrame and mask determines 
        # to detect only that particular color 
        kernel = np.ones((5, 5), "uint8") 
        
        # For red color 
        red_mask = cv2.dilate(red_mask, kernel) 
        res_red = cv2.bitwise_and(imageFrame, imageFrame,  
                                mask = red_mask) 
        

        # Creating contour to track red color 
        contours, hierarchy = cv2.findContours(red_mask, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE) 
        
        maxArea = None
        maxContour = None
        for pic, contour in enumerate(contours): 
            area = cv2.contourArea(contour) 
            if(area > 900) and (maxArea is None or area > maxArea):
                maxArea = area
                maxContour = contour



        #If detect people and red, choose person with max overlap with red. if all have no overlap, choose red
        # if detect people and no red, choose first person
        # if detect red and no people, choose red





        if(maxContour is not None):
            
            # Inference
            results = model(frame)

            # Results
            labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
            n = len(labels)
            people = []
            for i in range(n):
                row = cord[i]
                label = results.names[int(labels[i])]
                if(label != 'person'):
                    continue
                


                x1, y1, x2, y2 = int(row[0]*frame.shape[1]), int(row[1]*frame.shape[0]), int(row[2]*frame.shape[1]), int(row[3]*frame.shape[0])

                people.append((x1,y1,x2-x1,y2-y1))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)                
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            
                


            
            a, b, c, d = target_region
            cv2.rectangle(frame, (int(a), int(b)), (int(a + c), int(b + d)), (0, 255, 0), 2)
            cv2.putText(frame, "Target", (int(a), int(b)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, 
                        (0, 255,0))  
            


            data_out = calculateCommands((x1,y1,x2-x1,y2-y1),drone_id, target_region,(width,height))
            #print(data_out['drones'][drone_id])
            export(data_out,'data.json')









            x, y, w, h = cv2.boundingRect(maxContour) 
            imageFrame = cv2.rectangle(imageFrame, (x, y),  
                                    (x + w, y + h),  
                                    (0, 0, 255), 2) 
            
            cv2.putText(imageFrame, "Red Colour", (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                        (0, 0, 255))     
            
            
            red = (x,y,w,h)

            calc_data = (0,0,0,0)
            if len(people) == 0:
                calc_data = red
            else:
                intersects = {}
                
                for person in people:
                    intersects[person] = intersection(red,person,width,height)
                
                max_person = None
                max_inter = 0
                for p,v in intersects.items():
                    if v > max_inter:
                        max_person = p
                        max_inter = v
                
                if max_person == None:
                    calc_data = red
                else:
                    calc_data = max_person

            

            x, y, w, h = calc_data

            imageFrame = cv2.rectangle(imageFrame, (x, y),  
                                    (x + w, y + h),  
                                    (255, 0, 0), 3) 
            
            cv2.putText(imageFrame, "Tracking Object", (x, y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                        (255, 0, 0))     
            







            

            data_out = calculateCommands(calc_data,drone_id, target_region,(width,height))
            print(data_out['drones'][drone_id])
            export(data_out,'data.json')













        # Program Termination 
        cv2.imshow("Multiple Color Detection in Real-Time", frame) 
        if cv2.waitKey(10) & 0xFF == ord('q'): 
            cv2.destroyAllWindows() 
            break


def intersection(A,B, ww, wh):
    x0, y0, w0, h0 = A
    x1, y1, w1, h1 = B
    # Calculate the (x, y) coordinates of the intersection rectangle
    intersect_top_left_x = max(x0, x1)
    intersect_top_left_y = max(y0, y1)
    intersect_bottom_right_x = min(x0 + w0, x1 + w1)
    intersect_bottom_right_y = min(y0 + h0, y1 + h1)

    # Calculate the width and height of the intersection rectangle
    width = intersect_bottom_right_x - intersect_top_left_x
    height = intersect_bottom_right_y - intersect_top_left_y

    # Check if there is an intersection
    if width > 0 and height > 0:
        return (width * height)/(ww*wh)
    else:
        return 0
    


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