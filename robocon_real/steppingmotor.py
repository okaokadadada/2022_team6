from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

CW=17
CCW=23

#GPIOの設定
GPIO.setmode(GPIO.BCM)              #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(CW, GPIO.OUT)          #GPIO27を出力モードに設定
GPIO.setup(CCW, GPIO.OUT)           #GPIO18を入力モードに設定

while True:
  try:
    
    GPIO.output(CCW,GPIO.LOW)
    GPIO.output(CW, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
    time.sleep(0.00001)                     #10μ秒間待つ
    GPIO.output(CW, GPIO.LOW)               #GPIO27の出力をLow(0V)にする
    time.sleep(0.00001) 
    
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
