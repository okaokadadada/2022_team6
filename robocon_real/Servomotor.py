import RPi.GPIO as GPIO
import time

INTERVAL = 1
PIN = 14
FREQ = 50

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN, GPIO.OUT)
servo = GPIO.PWM(PIN, FREQ)

#init
servo.start(0.0)

servo.ChangeDutyCycle(2.5) #0度の位置まで動かす
time.sleep(INTERVAL)

servo.ChangeDutyCycle(9.1) #180度の位置まで動かす
time.sleep(INTERVAL)
  
GPIO.cleanup()
