import RPi.GPIO as GPIO
import time

INTERVAL =0.5
PIN = 14
FREQ = 50

# GPIO.cleanup()

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN, GPIO.OUT)
servo = GPIO.PWM(PIN, FREQ)

servo.start(0.0)

# servo.ChangeDutyCycle(8.0)

for i in range(2):#初期の9.1から2.5まで動かす
 for i in range(70):
   servo.ChangeDutyCycle(9.5-0.1*i)
   time.sleep(INTERVAL)
  
 time.sleep(0.5)

 for i in range(70):
   servo.ChangeDutyCycle(2.5+0.1*i)
   time.sleep(INTERVAL)

 time.sleep(0.5)

GPIO.cleanup()
