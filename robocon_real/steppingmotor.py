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
GPIO.setup(CW, GPIO.OUT)          #GPIO27を出力モードに設定
GPIO.setup(CCW, GPIO.OUT)           #GPIO18を入力モードに設定

while True:
  try:
    for i in range(1000):
      GPIO.output(CWp,HIGH)
      GPIO.output(CWm, LOW)            #GPIO27の出力をHigh(3.3V)にする
      time.sleep(0.005)
    for i in range(1000):
      GPIO.output(CCWp,HIGH)
      GPIO.output(CCWm, LOW)            #GPIO27の出力をHigh(3.3V)にする
      time.sleep(0.005)
    
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
