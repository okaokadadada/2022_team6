from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

CWp=17
CWm=3
CCWp=23
CCWm=4

#GPIOの設定
GPIO.setmode(GPIO.BCM)              #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(CWp, GPIO.OUT)          #GPIO27を出力モードに設定
#GPIO.setup(CWm, GPIO.OUT)          #GPIO27を出力モードに設定
#GPIO.setup(CCWp, GPIO.OUT)           #GPIO18を入力モードに設定
#GPIO.setup(CCWm, GPIO.OUT)

while True:
  try:
    for i in range(1000):
      GPIO.output(CWp, GPIO.HIGH)
      #GPIO.output(CWm, GPIO.LOW)            #GPIO27の出力をHigh(3.3V)にする
      time.sleep(1)
      GPIO.output(CWp, GPIO.LOW)
      #GPIO.output(CWm, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
      time.sleep(1)
    #for i in range(1000):
      #GPIO.output(CCWp, GPIO.HIGH)
      #GPIO.output(CCWm, GPIO.LOW)            #GPIO27の出力をHigh(3.3V)にする
      #time.sleep(0.005)
      #GPIO.output(CCWp, GPIO.LOW)
      #GPIO.output(CCWm, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
      #time.sleep(0.005)
    
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
