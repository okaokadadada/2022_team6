# sample program for 28BYJ-48 and ULN2003
import RPi.GPIO as GPIO
import time

right_IN1 = 17
right_IN2 = 22
right_IN3 = 23
right_IN4 = 24

left_IN1 = 
left_IN2 = 
left_IN3 = 
left_IN4 = 

WAITTIME = 0.002

GPIO.setmode( GPIO.BCM )
GPIO.cleanup()
GPIO.setup( right_IN1, GPIO.OUT )　#右ステッピングモータを出力に設定
GPIO.setup( right_IN2, GPIO.OUT )
GPIO.setup( right_IN3, GPIO.OUT )
GPIO.setup( right_IN4, GPIO.OUT )

GPIO.setup( left_IN1, GPIO.OUT )　#左ステッピングモータを出力に設定
GPIO.setup( left_IN2, GPIO.OUT )
GPIO.setup( left_IN3, GPIO.OUT )
GPIO.setup( left_IN4, GPIO.OUT )

#右，左ステッピングモータを停止させる関数
def right_stop():
  GPIO.output( right_IN1, GPIO.LOW )
  GPIO.output( right_IN2, GPIO.LOW )
  GPIO.output( right_IN3, GPIO.LOW )
  GPIO.output( right_IN4, GPIO.LOW )

def left_stop():
  GPIO.output( left_IN1, GPIO.LOW )
  GPIO.output( left_IN2, GPIO.LOW )
  GPIO.output( left_IN3, GPIO.LOW )
  GPIO.output( left_IN4, GPIO.LOW )

#右ステッピングモータの出力を決定する関数，正回転させる関数，逆回転させる関数
def setStep( w1, w2, w3, w4 ):
  GPIO.output( right_IN1, w1 )
  GPIO.output( right_IN2, w2 )
  GPIO.output( right_IN3, w3 )
  GPIO.output( right_IN4, w4 )
  time.sleep( WAITTIME )

def right_advance( angle ):
  for i in range(0,int(angle * 1.422222222)):
    setStep( 1, 0, 0, 0 )
    setStep( 0, 1, 0, 0 )
    setStep( 0, 0, 1, 0 )
    setStep( 0, 0, 0, 1 )

def right_back( angle ):
  for i in range(0,int(angle * 1.422222222)):
    setStep( 0, 0, 0, 1 )
    setStep( 0, 0, 1, 0 )
    setStep( 0, 1, 0, 0 )
    setStep( 1, 0, 0, 0 )

#左ステッピングモータの出力を決定する関数，正回転させる関数，逆回転させる関数
def setStep( w1, w2, w3, w4 ):
  GPIO.output( left_IN1, w1 )
  GPIO.output( left_IN2, w2 )
  GPIO.output( left_IN3, w3 )
  GPIO.output( left_IN4, w4 )
  time.sleep( WAITTIME )

def left_advance( angle ):
  for i in range(0,int(angle * 1.422222222)):
    setStep( 1, 0, 0, 0 )
    setStep( 0, 1, 0, 0 )
    setStep( 0, 0, 1, 0 )
    setStep( 0, 0, 0, 1 )

def left_back( angle ):
  for i in range(0,int(angle * 1.422222222)):
    setStep( 0, 0, 0, 1 )
    setStep( 0, 0, 1, 0 )
    setStep( 0, 1, 0, 0 )
    setStep( 1, 0, 0, 0 )
    
# main
count = 0
try:
  while count<3:
    right_advance( 3600 )
    left_advance( 3600 )
    time.sleep( 0.5 )  #前進
    
    right_back( 3600 )
    left_back( 3600 )
    time.sleep( 0.5 )　#後退
    
    count = count + 1
    print( count )
    
except KeyboardInterrupt:
  GPIO.cleanup()
  print("cleanup")
