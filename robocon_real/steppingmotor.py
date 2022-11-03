from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート
import threading

#モータのGPIO設定
CWp_R=16
CWm_R=19
CCWp_R=20
CCWm_R=21
CWp_L=12
CWm_L=6
CCWp_L=5
CCWm_L=7

waittime_R = 0.005
waittime_L = 0.005
waittime = 0.01

#モータのGPIO設定
GPIO.setmode(GPIO.BCM)               #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(CWp_R, GPIO.OUT)
GPIO.setup(CWm_R, GPIO.OUT)
GPIO.setup(CCWp_R, GPIO.OUT)
GPIO.setup(CCWm_R, GPIO.OUT)
GPIO.setup(CWp_L, GPIO.OUT)
GPIO.setup(CWm_L, GPIO.OUT)
GPIO.setup(CCWp_L, GPIO.OUT)
GPIO.setup(CCWm_L, GPIO.OUT)

def right_G():  #右ステッピングモータを正転させる関数
  while True:
    for i in range(2000):
      GPIO.output(CCWp_R, GPIO.HIGH)
      GPIO.output(CCWm_R, GPIO.LOW)             #CWをONに
      time.sleep(waittime_R/(2000-i))
      GPIO.output(CCWp_R, GPIO.LOW)
      GPIO.output(CCWm_R, GPIO.HIGH)            #CWをOFFに
      time.sleep(waittime_R/(2000-i))
    for i in range(2000):
      GPIO.output(CCWp_R, GPIO.HIGH)
      GPIO.output(CCWm_R, GPIO.LOW)             #CWをONに
      time.sleep(waittime_R)
      GPIO.output(CCWp_R, GPIO.LOW)
      GPIO.output(CCWm_R, GPIO.HIGH)            #CWをOFFに
      time.sleep(waittime_R)
    for i in range(2000):
      GPIO.output(CCWp_R, GPIO.HIGH)
      GPIO.output(CCWm_R, GPIO.LOW)             #CWをONに
      time.sleep(waittime_R/(i+1))
      GPIO.output(CCWp_R, GPIO.LOW)
      GPIO.output(CCWm_R, GPIO.HIGH)            #CWをOFFに
      time.sleep(waittime_R/(i+1))
    
    #for i in range(100):
    #  GPIO.output(CWp_R, GPIO.HIGH)
   #   GPIO.output(CWm_R, GPIO.LOW)             #CCWをONに
   #   time.sleep(waittime_R)
   #   GPIO.output(CWp_R, GPIO.LOW)
   #   GPIO.output(CWm_R, GPIO.HIGH)            #CCWをOFFに
   #   time.sleep(waittime_R)
   # time.sleep(1)
    
def right_B():  #右ステッピングモータを逆転させる関数
  while True:
    GPIO.output(CCWp_R, GPIO.HIGH)
    GPIO.output(CCWm_R, GPIO.LOW)             #CCWをONに
    time.sleep(waittime)
    GPIO.output(CCWp_R, GPIO.LOW)
    GPIO.output(CCWm_R, GPIO.HIGH)            #CCWをOFFに
    time.sleep(waittime)
    
def left_G():   #左ステッピングモータを正転させる関数
  while True:
    for i in range(2000):
      GPIO.output(CWp_L, GPIO.HIGH)
      GPIO.output(CWm_L, GPIO.LOW)             #CWをONに
      time.sleep(waittime_L/(2000-i))
      GPIO.output(CWp_L, GPIO.LOW)
      GPIO.output(CWm_L, GPIO.HIGH)            #CWをOFFに
      time.sleep(waittime_L/(2000-i))
    for i in range(2000):
      GPIO.output(CWp_L, GPIO.HIGH)
      GPIO.output(CWm_L, GPIO.LOW)             #CWをONに
      time.sleep(waittime_L)
      GPIO.output(CWp_L, GPIO.LOW)
      GPIO.output(CWm_L, GPIO.HIGH)            #CWをOFFに
      time.sleep(waittime_L)
    for i in range(2000):
      GPIO.output(CWp_L, GPIO.HIGH)
      GPIO.output(CWm_L, GPIO.LOW)             #CWをONに
      time.sleep(waittime_L/(i+1))
      GPIO.output(CWp_L, GPIO.LOW)
      GPIO.output(CWm_L, GPIO.HIGH)            #CWをOFFに
      time.sleep(waittime_L/(i+1))
   # for i in range(100):
   #   GPIO.output(CCWp_L, GPIO.HIGH)
   #   GPIO.output(CCWm_L, GPIO.LOW)             #CCWをONに
   #   time.sleep(waittime_L)
   #   GPIO.output(CCWp_L, GPIO.LOW)
   #   GPIO.output(CCWm_L, GPIO.HIGH)            #CCWをOFFに
   #   time.sleep(waittime_L) 
   # time.sleep(1)
    
def left_B():   #左ステッピングモータを逆転させる関数
  while True:
    GPIO.output(CCWp_L, GPIO.HIGH)
    GPIO.output(CCWm_L, GPIO.LOW)             #CCWをONに
    time.sleep(waittime)
    GPIO.output(CCWp_L, GPIO.LOW)
    GPIO.output(CCWm_L, GPIO.HIGH)            #CCWをOFFに
    time.sleep(waittime)
  
try:
    if __name__ == "__main__":
        thread_2 = threading.Thread(target=right_G)
        thread_3 = threading.Thread(target=left_G)
        
        thread_2.start()
        thread_3.start()

except KeyboardInterrupt:       #Ctrl+Cキーが押された
        GPIO.cleanup()              #GPIOをクリーンアップ
        sys.exit()                  #プログラム終了
