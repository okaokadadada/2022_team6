import RPi.GPIO as GPIO
import time

INTERVAL = 0.6
PIN = 14
FREQ = 50

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN, GPIO.OUT)
servo = GPIO.PWM(PIN, FREQ)

#init
servo.start(0.0)

for i in range(2):
  servo.ChangeDutyCycle(2.5)
  time.sleep(INTERVAL)

  servo.ChangeDutyCycle(16.75)
  time.sleep(INTERVAL)
  
GPIO.cleanup()
