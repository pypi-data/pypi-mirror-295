import cv2
import numpy as np

def detect_color(frame, color):

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if color == 'Orange':
        lower_bound = np.array([10, 100, 20]) 
        upper_bound = np.array([25, 255, 255])  
    elif color == 'Merah':
        lower_bound = np.array([0, 100, 100])  
        upper_bound = np.array([10, 255, 255])  
    elif color == 'Biru':
        lower_bound = np.array([100, 150, 0])  
        upper_bound = np.array([140, 255, 255])  
    else:
        raise ValueError("Salah warna ui!")

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    return result

def detectOrange(frame):
    return detect_color(frame, 'Orange')

def detectMerah(frame):
    return detect_color(frame, 'Merah')

def detectBiru(frame):
    return detect_color(frame, 'Biru')
