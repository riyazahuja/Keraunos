import numpy as np
import cv2
import mss
import pywinctl as pw
from datetime import datetime
import json
from math import exp, ceil




path = 'data.json'

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


    windows = pw.getWindowsWithTitle(app_title)

    # Check if any window matched
    if not windows:
        print(f"No windows found with title: {app_title}")
        return
    

    window = windows[0]
    window.activate()

    with mss.mss() as sct:
        # Define the bounding box of the window
        monitor = {"top": window.top, "left": window.left, "width": window.width, "height": window.height}
        width = window.width
        height = window.height
        target_region = get_target_region(width, height, (0.25,0.25), (0.75,0.75))

        while True:
            sct_img = sct.grab(monitor)
            imageFrame = np.array(sct_img)

            # Convert to BGR format for OpenCV
            imageFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGRA2BGR)



            # Your existing processing code starts here
            # Convert the imageFrame in BGR(RGB color space) to HSV(hue-saturation-value) color space
            hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
            frame= imageFrame
            #imageFrame=hsvFrame


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
                if(area > 600) and (maxArea is None or area > maxArea):
                    maxArea = area
                    maxContour = contour
            if(maxContour is not None):
                x, y, w, h = cv2.boundingRect(maxContour) 
                imageFrame = cv2.rectangle(imageFrame, (x, y),  
                                        (x + w, y + h),  
                                        (0, 0, 255), 2) 
                
                cv2.putText(imageFrame, "Red Colour", (x, y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                            (0, 0, 255))     
                
                a, b, c, d = target_region
                cv2.rectangle(imageFrame, (int(a), int(b)), (int(a + c), int(b + d)), (0, 255, 0), 2)
                cv2.putText(imageFrame, "Target", (int(a), int(b)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                            (0, 255,0))  
                

                course_correction = calculate_cc((x,y,w,h),drone_id, target_region,(width,height))

                data_out = merge(course_correction,drone_id)




                # Pull in json data, copy data from leader drone, weighted average based on 
                # difference of time stamp of current commands and leader drone command.

                print(data_out[drone_id])
                export(data_out, path)



            # Program Termination 
            cv2.imshow("Multiple Color Detection in Real-Time", imageFrame) 
            if cv2.waitKey(10) & 0xFF == ord('q'): 
                cv2.destroyAllWindows() 
                break



#dropoff function:
#f(x) = -100e^{-0.1*x}+100
def plateau_and_round(x):
    return ceil(-100 * exp(-0.1 * x)+100)


def calculate_cc(actual_region, drone_id, target_region, window):
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

    

    return data

def import_json_data(path):
    try:
        with open(path, 'r') as file:
            fc = json.load(file)
            return fc
    except:
        return None

def merge(course_correction, drone_id, path = path):
    leader_data = import_json_data(path)
    if leader_data is None:
        # Leader drone not turned on yet.
        return course_correction
    try:
        leader_data = leader_data['drones']['1']
    except:
        leader_data = leader_data['drones'][1]

        
    self_data = course_correction[drone_id]

    leader_time, self_time = datetime.fromisoformat(leader_data['time']), datetime.fromisoformat(self_data['time'])
    sec = (leader_time-self_time).total_seconds()
    td = abs(sec)
    tw = exp(-4 * td)

    w = lambda name: (lambda weight: (tw*weight) * self_data[name] + (1-tw*weight)*leader_data[name])

    data = {
        drone_id : {
            'time': datetime.now().isoformat(),
            'role': self_data['role'],
            'turnl': w('turnl')(0.25),
            'turnr': w('turnr')(0.25),
            'up': w('up')(0.25),
            'down': w('down')(0.25),
            'forward': w('forward')(0.1),
            'back': w('back')(0.1)
        }
    }
    return data

def export(data,path):
    try:
        fc = import_json_data(path)

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


capture_app_window(1)