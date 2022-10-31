from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

CWp=16  #25  #0
CWm=19  #8  #5
CCWp=20  #7  #6
CCWm=21  #1  #13

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
      time.sleep(0.05)
      GPIO.output(CWp, GPIO.LOW)
      GPIO.output(CWm, GPIO.HIGH)        #CW入力をOFFに
      time.sleep(0.1)
    for i in range(1000):
      GPIO.output(CCWp, GPIO.HIGH)
      GPIO.output(CCWm, GPIO.LOW)         #CW入力をONに
      time.sleep(0.1)
      GPIO.output(CCWp, GPIO.LOW)
      GPIO.output(CCWm, GPIO.HIGH)        #CW入力をOFFに
      time.sleep(0.1)
    
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
