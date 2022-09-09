#!/usr/bin/python
import time
import RPi.GPIO as GPIO
 
ENable    =  4 #07pin
CW = 17 #11pin# 1=CW,0=CCW
CLK     = 18 #12pin
#MicroStep M1=1 M2=1 M3=0 ...1/16
 
#init
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENable , GPIO.OUT)
GPIO.output(ENable , 0)
GPIO.setup(CW , GPIO.OUT)
GPIO.setup(CLK , GPIO.OUT)
pwm = GPIO.PWM(CLK, 100) #100Hz Max 200kHz
pwm.start(50) #duty 50%
 
 
def forward(speed):
        GPIO.output(CW , 1)
        GPIO.output(ENable , 1)
        print ("forward ",speed)
        pwm.ChangeFrequency(speed/3) #
        time.sleep(0.1)
        pwm.ChangeFrequency(speed)
 
def backwards(speed):
        GPIO.output(CW, 0)
        GPIO.output(ENable , 1)
        print ("backwards",speed)
        pwm.ChangeFrequency(speed/3)
        time.sleep(0.1)
        pwm.ChangeFrequency(speed)
 
def Stop():
        GPIO.output(ENable , 0)
        pwm.stop()
 
#main
try:
        print ("start")
        forward(8000) #1000 is 1kHz
        time.sleep(5)
        backwards(2000)
        time.sleep(5)
        Stop()
        GPIO.cleanup()
except:
        print ("Done!")
        Stop()
        GPIO.cleanup()
