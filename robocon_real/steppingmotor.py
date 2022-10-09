from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

CWp_R=2
CWm_R=3
CCWp_R=4
CCWm_R=14
CWp_L=15
CWm_L=18
CCWp_L=17
CCWm_L=27

#GPIOの設定
GPIO.setmode(GPIO.BCM)               #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(CWp_R, GPIO.OUT)            #GPIO17を出力モードに設定
GPIO.setup(CWm_R, GPIO.OUT)            #GPIO3を出力モードに設定
GPIO.setup(CCWp_R, GPIO.OUT)           #GPIO23を出力モードに設定
GPIO.setup(CCWm_R, GPIO.OUT)           #GPIO4を出力モードに設定
GPIO.setup(CWp_L, GPIO.OUT)            #GPIO17を出力モードに設定
GPIO.setup(CWm_L, GPIO.OUT)            #GPIO3を出力モードに設定
GPIO.setup(CCWp_L, GPIO.OUT)           #GPIO23を出力モードに設定
GPIO.setup(CCWm_L, GPIO.OUT)           #GPIO4を出力モードに設定

a=0.0004

while True:
  try:
    a=0
    b=0
    for i in range(2000):
      GPIO.output(CWp_R, GPIO.HIGH)
      GPIO.output(CWm_R, GPIO.LOW)            #CCWをONに
      GPIO.output(CWp_L, GPIO.HIGH)
      GPIO.output(CWm_L, GPIO.LOW)
      time.sleep(0.0005)
      GPIO.output(CWp_R, GPIO.LOW)
      GPIO.output(CWm_R, GPIO.HIGH)           #CCWをOFFに
      GPIO.output(CWp_L, GPIO.LOW)
      GPIO.output(CWm_L, GPIO.HIGH)
      time.sleep(0.0005)
      a=a+1
      print("a=",a)
    #for j in range(2000):
     # GPIO.output(CCWp_R, GPIO.HIGH)
     # GPIO.output(CCWm_R, GPIO.LOW)            #CCWをONに
     # GPIO.output(CCWp_L, GPIO.HIGH)
     # GPIO.output(CCWm_L, GPIO.LOW)
     # time.sleep(0.0005)
     # GPIO.output(CCWp_R, GPIO.HIGH)
     # GPIO.output(CCWm_R, GPIO.LOW)           #CCWをOFFに
     # GPIO.output(CCWp_L, GPIO.HIGH)
     # GPIO.output(CCWm_L, GPIO.LOW)
     # time.sleep(0.0005)
     # b=b+1
     # print("b=",b)
    
  except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
