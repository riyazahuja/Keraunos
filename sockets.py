import numpy as np 
import cv2 
  
  
# Capturing video through webcam 
webcam = cv2.VideoCapture(0) 
  
# Start a while loop 
while(1): 
      
    # Reading the video from the 
    # webcam in image frames 
    _, imageFrame = webcam.read() 
  
    # Convert the imageFrame in  
    # BGR(RGB color space) to  
    # HSV(hue-saturation-value) 
    # color space 
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

    # # Set range for custom color and
    # # define mask
    # custom_lower = np.array([_, _, _], np.uint8)
    # custom_upper = np.array([_, _, _], np.uint8)
    # custom_mask = cv2.inRange(hsvFrame, custom_lower, custom_upper)

    # Morphological Transform, Dilation 
    # for each color and bitwise_and operator 
    # between imageFrame and mask determines 
    # to detect only that particular color 
    kernel = np.ones((5, 5), "uint8")

    # # For custom color
    # custom_mask = cv2.dilate(custom_mask, kernel)
    # res_custom = cv2.bitwise_and(imageFrame, imageFrame,
    #                              mask = custom_mask)
      
    # # Creating contour to track custom color
    # contours, hierarchy = cv2.findContours(custom_mask,
    #                                        cv2.RETR_TREE,
    #                                        cv2.CHAIN_APPROX_SIMPLE)
    
    # maxArea = None
    # maxContour = None
    # for pic, contour in enumerate(contours):
    #     area = cv2.contourArea(contour)
    #     if(area > 900) and (maxArea is None or area > maxArea):
    #         maxArea = area
    #         maxContour = contour

    # if(maxContour is None):
    #     pass
        
    # x, y, w, h = cv2.boundingRect(maxContour)
    # imageFrame = cv2.rectangle(imageFrame, (x, y),
    #                             (x + w, y + h),
    #                             (_, _, _), 2)
    
    # cv2.putText(imageFrame, "Custom Color", (x, y),
    #             cv2.FONT_HERSHEY_SIMPLEX, 1.0,
    #             (_, _, _))
                 
    # Program Termination 
    cv2.imshow("Custom Color Detection in Real-TIme", imageFrame) 
    if cv2.waitKey(10) & 0xFF == ord('q'): 
        cv2.destroyAllWindows() 
        break