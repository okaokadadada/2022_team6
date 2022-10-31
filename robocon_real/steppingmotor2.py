from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

CWp=0  #25
CWm=5  #8
CCWp=6  #7
CCWm=13  #1

#GPIOの設定
GPIO.setmode(GPIO.BCM)               #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(CWp, GPIO.OUT)            #GPIO17を出力モードに設定
GPIO.setup(CWm, GPIO.OUT)            #GPIO3を出力モードに設定
GPIO.setup(CCWp, GPIO.OUT)           #GPIO23を出力モードに設定
GPIO.setup(CCWm, GPIO.OUT)           #GPIO4を出力モードに設定

time.sleep(0.15)

while True:
  try:
    for i in range(1000):
      GPIO.output(CWp, GPIO.HIGH)
      GPIO.output(CWm, GPIO.LOW)         #CW入力をONに
      time.sleep(0.005)
      GPIO.output(CWp, GPIO.LOW)
      GPIO.output(CWm, GPIO.HIGH)        #CW入力をOFFに
      time.sleep(0.005)
    for i in range(1000):
      GPIO.output(CWp, GPIO.HIGH)
      GPIO.output(CWm, GPIO.LOW)         #CW入力をONに
      time.sleep(0.005)
      GPIO.output(CWp, GPIO.LOW)
      GPIO.output(CWm, GPIO.HIGH)        #CW入力をOFFに
      time.sleep(0.005)
    
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
