#必要なモジュールをインポート
from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

#ポート番号の定義
Trig = 27                           #変数"Trig"に27を代入
Echo = 18                           #変数"Echo"に18を代入

sig_on = 0
sig_off = 0

#GPIOの設定
GPIO.setmode(GPIO.BCM)              #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(Trig, GPIO.OUT)          #GPIO27を出力モードに設定
GPIO.setup(Echo, GPIO.IN)           #GPIO18を入力モードに設定

#HC-SR04で距離を測定する関数
def read_distance():

    global sig_on
    global sig_off

    GPIO.output(Trig, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
    time.sleep(0.00001)                     #10μ秒間待つ
    GPIO.output(Trig, GPIO.LOW)             #GPIO27の出力をLow(0V)にする

    while GPIO.input(Echo) == GPIO.LOW:     #GPIO18がLowの時間
        sig_off = time.time()
    while GPIO.input(Echo) == GPIO.HIGH:    #GPIO18がHighの時間
        sig_on = time.time()


    duration = sig_off - sig_on             #GPIO18がHighしている時間を算術
    distance = duration * 34000 / 2         #距離を求める(cm)
    return distance
    cm = -read_distance()
    
# sample program for 28BYJ-48 and ULN2003　　　#ステッピングモータ

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

def right():
  while True:
    setStep( 1, 0, 0, 0 )
    setStep( 0, 1, 0, 0 )
    setStep( 0, 0, 1, 0 )
    setStep( 0, 0, 0, 1 )
    if cm>100:
      break

def left():
  while True:
    setStep( 0, 0, 0, 1 )
    setStep( 0, 0, 1, 0 )
    setStep( 0, 1, 0, 0 )
    setStep( 1, 0, 0, 0 )
    if cm<100:
      break

# main
initialize()
count = 0
try:
  while True:
    right()
    time.sleep( 0.5 )
    left()
    time.sleep( 0.5 )
#ステッピングモータ

except KeyboardInterrupt:       #Ctrl+Cキーが押された
        GPIO.cleanup()              #GPIOをクリーンアップ
        print("cleanup")
        sys.exit()                  #プログラム終了
