from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

CWp=17
CWm=3
CCWp=23
CCWm=4

#GPIOの設定
GPIO.setmode(GPIO.BCM)               #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(CWp, GPIO.OUT)            #GPIO17を出力モードに設定
GPIO.setup(CWm, GPIO.OUT)            #GPIO3を出力モードに設定
GPIO.setup(CCWp, GPIO.OUT)           #GPIO23を出力モードに設定
GPIO.setup(CCWm, GPIO.OUT)           #GPIO4を出力モードに設定

time.sleep(0.15)

while True:
  try:
    GPIO.output(CCWp, GPIO.HIGH)
    GPIO.output(CCWm, GPIO.LOW)          #CCW入力をONに
    for i in range(1000):
      GPIO.output(CWp, GPIO.HIGH)
      GPIO.output(CWm, GPIO.LOW)         #CW入力をONに
      time.sleep(0.05)
      GPIO.output(CWp, GPIO.LOW)
      GPIO.output(CWm, GPIO.HIGH)        #CW入力をOFFに
      time.sleep(0.05)
      
    GPIO.output(CCWp, GPIO.LOW)
    GPIO.output(CCWm, GPIO.HIGH)     　  #CCW入力をOFFに
    for i in range(1000):
      GPIO.output(CWp, GPIO.HIGH)
      GPIO.output(CWm, GPIO.LOW)         #CW入力をONに
      time.sleep(0.05)
      GPIO.output(CWp, GPIO.LOW)
      GPIO.output(CWm, GPIO.HIGH)        #CW入力をOFFに
      time.sleep(0.05)
    
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()