# sample program for 28BYJ-48 and ULN2003
import RPi.GPIO as GPIO
import time

IN1 = 17
IN2 = 22
IN3 = 23
IN4 = 24
WAITTIME = 0.002

def initialize():
  print( "initialize" )
  GPIO.setmode( GPIO.BCM )
  GPIO.cleanup()
  GPIO.setup( IN1, GPIO.OUT )
  GPIO.setup( IN2, GPIO.OUT )
  GPIO.setup( IN3, GPIO.OUT )
  GPIO.setup( IN4, GPIO.OUT )
  #
  GPIO.output( IN1, GPIO.LOW )
  GPIO.output( IN2, GPIO.LOW )
  GPIO.output( IN3, GPIO.LOW )
  GPIO.output( IN4, GPIO.LOW )

def setStep( w1, w2, w3, w4 ):
  GPIO.output( IN1, w1 )
  GPIO.output( IN2, w2 )
  GPIO.output( IN3, w3 )
  GPIO.output( IN4, w4 )
  time.sleep( WAITTIME )

def right( angle ):
  for i in range(0,int(angle * 1.422222222)):
    setStep( 1, 0, 0, 0 )
    setStep( 0, 1, 0, 0 )
    setStep( 0, 0, 1, 0 )
    setStep( 0, 0, 0, 1 )

def left( angle ):
  for i in range(0,int(angle * 1.422222222)):
    setStep( 0, 0, 0, 1 )
    setStep( 0, 0, 1, 0 )
    setStep( 0, 1, 0, 0 )
    setStep( 1, 0, 0, 0 )

# main
initialize()
count = 0
try:
  while count<3:
    right( 3600 )
    time.sleep( 0.5 )
    left( 3600 )
    time.sleep( 0.5 )
    count = count + 1
    print( count )
except KeyboardInterrupt:
  GPIO.cleanup()
  print("cleanup")
