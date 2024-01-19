import numpy as np
import cv2
import mss
import pywinctl as pw
from datetime import datetime
import json



def get_webcam():
    webcam = cv2.VideoCapture(1) 
    _, imageFrame = webcam.read() 
    return imageFrame




def capture_app_window(drone_id, app_title = 'DE FPV'):
    # Find windows with partial match of the title
    windows = pw.getWindowsWithTitle(app_title)

    # Check if any window matched
    if not windows:
        print(f"No windows found with title: {app_title}")
        return

    window = windows[0]
    #window.focus()

    with mss.mss() as sct:
        # Define the bounding box of the window
        monitor = {"top": window.top, "left": window.left, "width": window.width, "height": window.height}

        while True:
            sct_img = sct.grab(monitor)
            imageFrame = np.array(sct_img)

            # Convert to BGR format for OpenCV
            imageFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGRA2BGR)

            imageFrame = get_webcam()

            # Your existing processing code starts here
            # Convert the imageFrame in BGR(RGB color space) to HSV(hue-saturation-value) color space
            hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
            #imageFrame=hsvFrame

            # # Set range for custom color and define mask
            # custom_lower = np.array([_, _, _], np.uint8)
            # custom_upper = np.array([_, _, _], np.uint8)
            # custom_mask = cv2.inRange(hsvFrame, custom_lower, custom_upper)

            # Set range for red color and define mask
            red_lower = np.array([136, 87, 111], np.uint8)
            red_upper = np.array([180, 255, 255], np.uint8)
            red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
        
            # Set range for green color and  
            # define mask 
            #green_lower = np.array([25, 52, 72], np.uint8) 
            #green_upper = np.array([102, 255, 255], np.uint8) 
            #green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 
        
            # Set range for blue color and 
            # define mask 
            #blue_lower = np.array([94, 80, 2], np.uint8) 
            #blue_upper = np.array([120, 255, 255], np.uint8) 
            #blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper) 
            
            # Morphological Transform, Dilation 
            # for each color and bitwise_and operator 
            # between imageFrame and mask determines 
            # to detect only that particular color 
            kernel = np.ones((5, 5), "uint8") 

            # # For custom color 
            # custom_mask = cv2.dilate(custom_mask, kernel) 
            # res_custom = cv2.bitwise_and(imageFrame, imageFrame,  
            #                         mask = custom_mask) 
            
            # For red color 
            red_mask = cv2.dilate(red_mask, kernel) 
            res_red = cv2.bitwise_and(imageFrame, imageFrame,  
                                    mask = red_mask) 
            
            # For green color 
            #green_mask = cv2.dilate(green_mask, kernel) 
            #res_green = cv2.bitwise_and(imageFrame, imageFrame, 
            #                            mask = green_mask) 
            
            # For blue color 
            #blue_mask = cv2.dilate(blue_mask, kernel) 
            #res_blue = cv2.bitwise_and(imageFrame, imageFrame, 
            #                        mask = blue_mask) 
            
            # # Creating contour to track custom color 
            # contours, hierarchy = cv2.findContours(custom_mask, 
            #                                     cv2.RETR_TREE, 
            #                                     cv2.CHAIN_APPROX_SIMPLE) 
            
            # maxArea = None
            # maxContour = None
            # for pic, contour in enumerate(contours): 
            #     area = cv2.contourArea(contour) 
            #     if(area > 900) and (maxArea is None or area > maxArea): 
            #         maxArea = area
            #         maxContour = contour
            # if(maxContour is not None):
            #         x, y, w, h = cv2.boundingRect(contour) 
            #         imageFrame = cv2.rectangle(imageFrame, (x, y),  
            #                                 (x + w, y + h),  
            #                                 (_, _, _), 2) 
                    
            #         cv2.putText(imageFrame, "Red Colour", (x, y), 
            #                     cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
            #                     (_, _, _))     
        
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
            if(maxContour is not None):
                x, y, w, h = cv2.boundingRect(maxContour) 
                imageFrame = cv2.rectangle(imageFrame, (x, y),  
                                        (x + w, y + h),  
                                        (0, 0, 255), 2) 
                
                cv2.putText(imageFrame, "Red Colour", (x, y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                            (0, 0, 255))     
                
                print(f'x:{x}, y:{y}, w:{w}, h:{h}')
                #data_out = calculateCommands((x,y,w,h),drone_id)
                #export(data_out,'data.json')



        
            # Creating contour to track green color 
            # contours, hierarchy = cv2.findContours(green_mask, 
            #                                     cv2.RETR_TREE, 
            #                                     cv2.CHAIN_APPROX_SIMPLE) 
            
            # maxArea = None
            # maxContour = None
            # for pic, contour in enumerate(contours): 
            #     area = cv2.contourArea(contour) 
            #     if(area > 900) and (maxArea is None or area > maxArea):
            #         maxArea = area
            #         maxContour = contour
            # if(maxContour is not None):
            #     x, y, w, h = cv2.boundingRect(maxContour) 
            #     imageFrame = cv2.rectangle(imageFrame, (x, y),  
            #                             (x + w, y + h),  
            #                             (0, 255, 0), 2) 
                
            #     cv2.putText(imageFrame, "Green Colour", (x, y), 
            #                 cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
            #                 (0, 255, 0))     
        
            # # Creating contour to track blue color 
            # contours, hierarchy = cv2.findContours(blue_mask, 
            #                                     cv2.RETR_TREE, 
            #                                     cv2.CHAIN_APPROX_SIMPLE) 
            
            # maxArea = None
            # maxContour = None
            # for pic, contour in enumerate(contours): 
            #     area = cv2.contourArea(contour) 
            #     if(area > 900) and (maxArea is None or area > maxArea):
            #         maxArea = area
            #         maxContour = contour
            # if(maxContour is not None):
            #     x, y, w, h = cv2.boundingRect(maxContour) 
            #     imageFrame = cv2.rectangle(imageFrame, (x, y),  
            #                             (x + w, y + h),  
            #                             (255, 0, 0), 2) 
                
            #     cv2.putText(imageFrame, "Blue Colour", (x, y), 
            #                 cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
            #                 (255, 0, 0))     
                    
            # Program Termination 
            cv2.imshow("Multiple Color Detection in Real-Time", imageFrame) 
            if cv2.waitKey(10) & 0xFF == ord('q'): 
                cv2.destroyAllWindows() 
                break


def calculateCommands(actual_region, drone_id, target_region):
    x,y,w,h = actual_region
    x0,y0,w0,h0 = target_region
    role = 'LEADER' if drone_id == 1 else 'FOLLOWER'

    area = w*h
    area0 = w0*h0

    turnl,turnr,up,down,forward,back = 0
    
    if area < area0:
        forward = 1
    elif area > area0:
        back = 1
    
    if x<x0:
        turnr = 1
    elif x>x0:
        turnl = 1

    if y<y0:
        down = 1
    elif y>y0:
        up = 1

    data = {
        'time': datetime.now().isoformat(),
        'drone_id': drone_id,
        'role': role,
        'turnl': turnl,
        'turnr': turnr,
        'up': up,
        'down': down,
        'forward': forward,
        'back': back
    }

    return data


def export(data,path):
    try:
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"An error occurred: {e}")

    




def list_window_titles():
    windows = pw.getAllTitles()
    return windows

titles = list_window_titles()
for title in titles:
    print(title)


capture_app_window(1, "GitHub Desktop")