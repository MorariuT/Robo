import numpy as np
import cv2
import RPi.GPIO as GPIO
import time
import signal
import sys
import traceback


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    GPIO.cleanup()
    sys.exit(0)

def pwm_stanga(p1,sens,p2,viteza):
    #print("pwm_stanga " + str(viteza))
    if sens=="inainte":    
        GPIO.output(p1, GPIO.HIGH)
        p2.ChangeDutyCycle(100-viteza)
    elif sens=="inapoi":
        GPIO.output(p1, GPIO.LOW)
        p2.ChangeDutyCycle(viteza)
        
def pwm_dreapta(p3,sens,p4,viteza):
    #print("pwm_dreapta " + str(viteza))
    if sens=="inainte":    
        GPIO.output(p3, GPIO.HIGH)
        p4.ChangeDutyCycle(100-viteza)
    elif sens=="inapoi":
        GPIO.output(p3, GPIO.LOW)
        p4.ChangeDutyCycle(viteza)
        
#############################################main
        
        
        
try:
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')

    ia1_sens = 26 # HIGH pt inainte, LOW pt inapoi
    ib1 = 19 # PWM
    ia2_sens = 13 # HIGH pt inainte, LOW pt inapoi
    ib2 = 6 # PWM

    GPIO.setmode(GPIO.BCM)        
    GPIO.setup(ia1_sens, GPIO.OUT)  #ib1
    GPIO.setup(ib1, GPIO.OUT)  #ia1
    GPIO.setup(ia2_sens, GPIO.OUT)  #ib2
    GPIO.setup(ib2, GPIO.OUT)  #ia2

    #pt motorul din stanga
    # initializam PWM la 50hz
    m1_p1 = GPIO.output(ia1_sens, GPIO.LOW)
    m1_p2 = GPIO.PWM(ib1, 50)
    # pornim pe oprit
    m1_p2.start(0)
    
    
    
    #pt motorul din dreapta
    # initializam PWM la 50hz
    m2_p3 = GPIO.output(ia2_sens, GPIO.HIGH)
    m2_p4 = GPIO.PWM(ib2, 50)
    # pornim pe oprit
    m2_p4.start(100)
         
    

    # citim de la camera /dev/video0 in rez. 1280/780
    
    
    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 1280)
    video_capture.set(4, 780)
    
    while(True):

        ret, frame = video_capture.read()
        #frame = cv2.flip(frame, 1 )
    
    
        crop_img = frame[500:780, 140:1140]


        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        
        ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
        contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)
            if M['m00']==0: M['m00'] = 0.001
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            #cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
            #cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
            cv2.line(crop_img, (cx-1,cy-1),(cx+1,cy+1),(255,0,0),10)
            cv2.putText(crop_img, ' Punct urmarire', (cx+10,cy),
                        cv2.FONT_HERSHEY_SIMPLEX , 1, (255,0,0), 2, cv2.LINE_AA)
            
    
            cv2.drawContours(crop_img, contours, -1, (0,0,255), 3)
            
            cx /= 10
            #print("cx="+str(cx))
            viteza_stanga = (cx/100)*80-25
            viteza_dreapta = 30-viteza_stanga
            
            viteza_dreapta *= 1.2
            viteza_stanga *= 1.2
            
            
            if viteza_dreapta > 25: viteza_dreapta = 25
            if viteza_stanga > 25: viteza_stanga = 25
            
            if viteza_dreapta < -25: viteza_dreapta = -25
            if viteza_stanga < -25: viteza_stanga = -25
            
            cv2.line(crop_img, (500-int(viteza_stanga), 180),(500,180),(0,0,255),20)
            cv2.line(crop_img, (500,200),(500+int(viteza_dreapta), 200),(0,255,0),20)
            
            cv2.putText(crop_img, 'Viteza Stanga:' + str(int(viteza_stanga)), (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX , 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(crop_img, 'Viteza Dreapta:' + str(int(viteza_dreapta)), (50,80),
                        cv2.FONT_HERSHEY_SIMPLEX , 1, (0,255,0), 2, cv2.LINE_AA)
            
            
            
            #print("cx="+ str(cx) + "vs="+ str(viteza_stanga) + " vd="+ str(viteza_dreapta))
            if viteza_stanga < 0:
                pwm_stanga(ia1_sens,"inapoi",m1_p2,0-viteza_stanga)
            else:
                pwm_stanga(ia1_sens,"inainte",m1_p2,viteza_stanga)
                
                
            if viteza_dreapta < 0:
                pwm_dreapta(ia2_sens,"inapoi",m2_p4,0-viteza_dreapta)
            else:
                pwm_dreapta(ia2_sens,"inainte",m2_p4,viteza_dreapta)
            
        
              
            '''
            if cx >= 230:
                pwm_dreapta(ia2_sens,"inapoi",m2_p4,40)
                pwm_stanga(ia1_sens,"inainte",m1_p2,40)
                time.sleep(0.1)
                print("Dreapta")
            elif cx >= 180:
                pwm_dreapta(ia2_sens,"inainte",m2_p4,0)
                pwm_stanga(ia1_sens,"inainte",m1_p2,20)
                print("Dreapta")
                
            if cx < 180 and cx > 100:
                pwm_dreapta(ia2_sens,"inainte",m2_p4,20)
                pwm_stanga(ia1_sens,"inainte",m1_p2,20)
                print("Inainte")
                
                
            if cx <= 60:
                pwm_dreapta(ia2_sens,"inainte",m2_p4,40)
                pwm_stanga(ia1_sens,"inapoi",m1_p2,40)
                time.sleep(0.10)
                print("stanga")
            elif cx <= 100:
                pwm_dreapta(ia2_sens,"inainte",m2_p4,20)
                pwm_stanga(ia1_sens,"inainte",m1_p2,0)
                print("stanga")
               ''' 
               
                
        else:
            print("Fara Linie")
            pwm_dreapta(ia2_sens,"inainte",m2_p4,0)
            pwm_stanga(ia1_sens,"inainte",m1_p2,0)
                
            
        cv2.imshow('Vedere robot',crop_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

    '''
    #test inainte
    for i in range(10):
        pwm_dreapta(ia2_sens,"inainte",m2_p4,10*i)
        pwm_dreapta(ia1_sens,"inainte",m1_p2,10*i)
        time.sleep(1)

    #test inapoi
    for i in range(10):
        pwm_dreapta(ia2_sens,"inapoi",m2_p4,10*i)
        pwm_dreapta(ia1_sens,"inapoi",m1_p2,10*i)
        time.sleep(1)


    time.sleep(1)
    '''
    
    
    GPIO.cleanup()


except :
    GPIO.cleanup()
    error = traceback.format_exc()
    print(error)
    print("Robot Error:")
    #print(e)

