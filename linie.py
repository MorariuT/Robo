import RPi.GPIO as GPIO
from time import sleep

def fata(p1, p2, v):
    p1.start(0)
    p2.start(v)
   
def spate(p1, p2, v):
    p1.start(v)
    p2.start(0)

def stop(p1, p2):
    p1.start(0)
    p2.start(0)




ia1 = 4
ia2 = 17
ib1 = 27
ib2 = 22
is1 = 5
is2 = 6
viteza_curbe = 50
viteza_fata = 20


GPIO.setmode(GPIO.BCM)
GPIO.setup(ia1, GPIO.OUT)
GPIO.setup(ib1, GPIO.OUT)
GPIO.setup(ia2, GPIO.OUT);
GPIO.setup(ib2, GPIO.OUT)

GPIO.setwarnings(False)
pwm_ia1 = GPIO.PWM(ia1, 30)
pwm_ib1 = GPIO.PWM(ib1, 30)
pwm_ia2 = GPIO.PWM(ia2, 30)
pwm_ib2 = GPIO.PWM(ib2, 30)

GPIO.setup(is1, GPIO.IN);
GPIO.setup(is2, GPIO.IN); 


#GPIO.input(5)
while(True):
    s1 = GPIO.input(is1)
    s2 = GPIO.input(is2)
#    print("s1 = " + str(s1) + " " + "s2 = " + str(s2))
    if s1 == 0 and s2 == 0:
        fata(pwm_ia1,pwm_ib1, viteza_fata)
        fata(pwm_ia2, pwm_ib2, viteza_fata)
    if s1 == 0 and s2 == 1:
        spate(pwm_ia1, pwm_ib1, viteza_curbe)
        fata(pwm_ia2, pwm_ib2, viteza_curbe)
    if s1 == 1 and s2 == 0:
        fata(pwm_ia1, pwm_ib1, viteza_curbe)
        spate(pwm_ia2, pwm_ib2, viteza_curbe)
    if s1 == 1 and s2 == 1:
        stop(pwm_ia1, pwm_ib1)
        stop(pwm_ia2, pwm_ib2) 
   
