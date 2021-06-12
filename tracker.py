import cv2,time,pyfirmata
import numpy as np 
def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
port = pyfirmata.Arduino('COM7')
pin9_x = port.get_pin('d:9:s')
pin8_y = port.get_pin('d:8:s')
cap = cv2.VideoCapture(0)
cap.set(3, 600)
cap.set(4, 600)
_, frame = cap.read()
rows, cols, _ = frame.shape
x_medium = int(cols / 2)
y_medium = int(cols / 2)
w_medium = int(cols / 2)
h_medium = int(cols / 2)
dur = 0
gecici_x = 0
gecici_y = 0
x = 0
y = 0
w = 0
h = 0
while(True):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([161, 155, 84])
    upper_red = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    if dur == 0:
            gecici_x = x
            gecici_y = y
    try:
        contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        x,y,w,h = cv2.boundingRect(contours[0])
    except IndexError:
        pass
    #time.sleep(0.0001)
    if abs(x-gecici_x)<30:
        servo_x = _map(x, 0, 650, 180, 0)
        pin9_x.write(servo_x)
    if abs(y-gecici_y)<30:
        servo_y = _map(y, 0, 500, 180, 0)
        pin8_y.write(servo_y) 
    gecici_x = x
    gecici_y = y
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),3)
    cv2.imshow("mask",mask)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    dur += 1  
cv2.waitKey(0)
cv2.destroyAllWindows