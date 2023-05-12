import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

pwm1 = GPIO.PWM(7, 50)
pwm2 = GPIO.PWM(3, 50)
pwm1.start(0)
pwm2.start(0)
start1 = 50
start2 = 50
durat = 500
cenX = 360
cenY = 240
increment = 3
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
tracker = cv2.legacy.TrackerTLD_create()

def set_servo_position(servoNumber, position):
    duty = float(position) / 10.0 + 2.5
    if servoNumber == 1:
        pwm1.ChangeDutyCycle(duty)
    elif servoNumber == 2:
        pwm2.ChangeDutyCycle(duty)
    
    time.sleep(0.02)  # small delay to allow the servo to move

def smooth_servo_move(servoNumber, start_position, end_position, duration):
#    print("inside smooth")
    interval = 10  # ms
    steps = int(duration / interval)
    delta = float(end_position - start_position) / float(steps)
    position = start_position
    if servoNumber == 1:
        for i in range(steps):
            position += delta
            set_servo_position(1, position)
        set_servo_position(1, end_position)
    elif servoNumber == 2:
        for i in range(steps):
            position += delta
            set_servo_position(2, position)
        set_servo_position(2, end_position)
def coi(grade):
    if grade >= 90:
        return 90
    elif grade <= 0:
        return 0        
    else:
        return grade

def centreaza(x,y,w,h):
    global start1, end1, start2, end2
    centerX, centerY = x+w/2, y+h/2 
    print(centerX, "     ", centerY)
    if centerX > cenX+20:
        print("increase XX")
        end1 = start1+increment
        end1 =  coi(end1)
        if centerY > cenY+20:
            print("increase YY")
            end2 = start2-increment
            end2 = coi(end2)
            smooth_servo_move(1, start1, end1, durat)
            smooth_servo_move(2, start2, end2, durat)
            #move both
        elif centerY < cenY-20:
            print("decrease YY")
            end2 = start2+increment
            end2 = coi(end2)
            smooth_servo_move(1, start1, end1, durat)
            smooth_servo_move(2, start2, end2, durat)
        #move both
    elif centerX < cenX-20:
        print("decrease XX")
        end1 = start1-increment
        end1 = coi(end1)
        if centerY > cenY+20:
            print("increase YY")
            end2 = start2-increment
            end2 = coi(end2)
            smooth_servo_move(1, start1, end1, durat)
            smooth_servo_move(2, start2, end2, durat)
        #move both
        elif centerY < cenY-20:
            print("decrease YY")
            end2 = start2+increment
            end2 = coi(end2)
            smooth_servo_move(1, start1, end1, durat)
            smooth_servo_move(2, start2, end2, durat)
            #move both
    else:
        print("not doing anything coaeee")
    print(end2)   
    start1 = end1
    start2 = end2

#smooth_servo_move(1, 0, 50, 500)
#smooth_servo_move(2, 0, 50, 500)
time.sleep(2)
cap = cv2.VideoCapture(0) 
ret, frame = cap.read(0)#read once to find square
face_img = frame.copy()
face_rects = face_cascade.detectMultiScale(face_img) 
roi = []
for (x,y,w,h) in face_rects:
    roi.append(x)
    roi.append(y)
    roi.append(x+w)
    roi.append(y+h)
roi = tuple(roi)
ret = tracker.init(frame, roi)

while True:
    ret, frame = cap.read(0) #0?
    success, roi = tracker.update(frame)
    (x,y,w,h) = tuple(map(int,roi))
    if success:
        centreaza(x,y,w,h)
    time.sleep(0.5)
