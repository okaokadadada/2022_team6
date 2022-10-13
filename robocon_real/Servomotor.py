import RPi.GPIO as GPIO
import time

INTERVAL =0.1
PIN = 14
FREQ = 50

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN, GPIO.OUT)
servo = GPIO.PWM(PIN, FREQ)

#init
servo.start(0.0)

for i in range(2):#初期の9.1から2.5まで動かす
  for i in range(30):
    servo.ChangeDutyCycle(9.1-0.22*i)
    time.sleep(INTERVAL)

  for i in range(30)
  servo.ChangeDutyCycle(2.5+0.22*i)
  time.sleep(INTERVAL)

GPIO.cleanup()
