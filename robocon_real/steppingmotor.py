from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

CWp=17
CWm=3
CCWp=23
CCWm=4
a=0.05

#GPIOの設定
GPIO.setmode(GPIO.BCM)               #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(CWp, GPIO.OUT)            #GPIO17を出力モードに設定
GPIO.setup(CWm, GPIO.OUT)            #GPIO3を出力モードに設定
GPIO.setup(CCWp, GPIO.OUT)           #GPIO23を出力モードに設定
GPIO.setup(CCWm, GPIO.OUT)           #GPIO4を出力モードに設定

a=0.01

while True:
  try:
    for i in range(200):
      GPIO.output(CWp, GPIO.HIGH)
      GPIO.output(CWm, GPIO.LOW)             #CWをONに
      time.sleep(a)
      GPIO.output(CWp, GPIO.LOW)
      GPIO.output(CWm, GPIO.HIGH)            #CWをOFFに
      time.sleep(a)
    for i in range(20):
      GPIO.output(CCWp, GPIO.HIGH)
      GPIO.output(CCWm, GPIO.LOW)            #CCWをONに
      time.sleep(a)
      GPIO.output(CCWp, GPIO.LOW)
      GPIO.output(CCWm, GPIO.HIGH)           #CCWをOFFに
      time.sleep(a)
    
    print(a)
    a=a-0.005
    
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
