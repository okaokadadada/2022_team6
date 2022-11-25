from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート
import threading

#モータのGPIO設定
CWp_R=7
CWm_R=5
CCWp_R=6
CCWm_R=12
CWp_L=16
CWm_L=19
CCWp_L=20
CCWm_L=21


waittime_R = 0.005
waittime_L = 0.005
waittime = 0.005
starttime = 1
difference = 0.0025

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

def turn_R():
  for i in range(500,2000,2):
    GPIO.output(CWp_R, GPIO.HIGH)
    GPIO.output(CWm_R, GPIO.LOW)             #CWをONに
    time.sleep(waittime_R+difference+(starttime/(i+1)))
    GPIO.output(CWp_R, GPIO.LOW)
    GPIO.output(CWm_R, GPIO.HIGH)            #CWをOFFに
    time.sleep(waittime_R+difference+(starttime/(i+1)))
  while True:
    for i in range(100):
      GPIO.output(CWp_R, GPIO.HIGH)
      GPIO.output(CWm_R, GPIO.LOW)             #CWをONに
      time.sleep(waittime_R+difference)
      GPIO.output(CWp_R, GPIO.LOW)
      GPIO.output(CWm_R, GPIO.HIGH)            #CWをOFFに
      time.sleep(waittime_R+difference)

def turn_L():
  for i in range(500,2000,2):
    GPIO.output(CCWp_L, GPIO.HIGH)
    GPIO.output(CCWm_L, GPIO.LOW)             #CWをONに
    time.sleep(waittime_L+(starttime/(i+1)))
    GPIO.output(CCWp_L, GPIO.LOW)
    GPIO.output(CCWm_L, GPIO.HIGH)            #CWをOFFに
    time.sleep(waittime_L+(starttime/(i+1)))
  while True:
    for i in range(100):
      GPIO.output(CCWp_L, GPIO.HIGH)
      GPIO.output(CCWm_L, GPIO.LOW)             #CWをONに
      time.sleep(waittime_L)
      GPIO.output(CCWp_L, GPIO.LOW)
      GPIO.output(CCWm_L, GPIO.HIGH)            #CWをOFFに
      time.sleep(waittime_L)

def right_GA():  #右ステッピングモータを正転させる関数
  while True:
    for i in range(500,2000,2):
      GPIO.output(CWp_R, GPIO.HIGH)
      GPIO.output(CWm_R, GPIO.LOW)             #CWをONに
      time.sleep(waittime_R+(starttime/(i+1)))
      GPIO.output(CWp_R, GPIO.LOW)
      GPIO.output(CWm_R, GPIO.HIGH)            #CWをOFFに
      time.sleep(waittime_R+(starttime/(i+1)))
    print("accererarion")
    for i in range(500):
      GPIO.output(CWp_R, GPIO.HIGH)
      GPIO.output(CWm_R, GPIO.LOW)             #CWをONに
      time.sleep(waittime_R)
      GPIO.output(CWp_R, GPIO.LOW)
      GPIO.output(CWm_R, GPIO.HIGH)            #CWをOFFに
      time.sleep(waittime_R)
    for i in range(500,2000,2):
      GPIO.output(CWp_R, GPIO.HIGH)
      GPIO.output(CWm_R, GPIO.LOW)             #CWをONに
      time.sleep(waittime_R+(starttime/(2001-i)))
      GPIO.output(CWp_R, GPIO.LOW)
      GPIO.output(CWm_R, GPIO.HIGH)            #CWをOFFに
      time.sleep(waittime_R+(starttime/(2001-i)))
    
def right_B():  #右ステッピングモータを逆転させる関数
  while True:
    GPIO.output(CCWp_R, GPIO.HIGH)
    GPIO.output(CCWm_R, GPIO.LOW)             #CCWをONに
    time.sleep(waittime)
    GPIO.output(CCWp_R, GPIO.LOW)
    GPIO.output(CCWm_R, GPIO.HIGH)            #CCWをOFFに
    time.sleep(waittime)
    
def left_GA():   #左ステッピングモータを正転させる関数
  while True:
    for i in range(500,2000,2):
      GPIO.output(CWp_L, GPIO.HIGH)
      GPIO.output(CWm_L, GPIO.LOW)             #CWをONに
      time.sleep(waittime_L+(starttime/(i+1)))
      GPIO.output(CWp_L, GPIO.LOW)
      GPIO.output(CWm_L, GPIO.HIGH)            #CWをOFFに
      time.sleep(waittime_L+(starttime/(i+1)))
    for i in range(500):
      GPIO.output(CWp_L, GPIO.HIGH)
      GPIO.output(CWm_L, GPIO.LOW)             #CWをONに
      time.sleep(waittime_L)
      GPIO.output(CWp_L, GPIO.LOW)
      GPIO.output(CWm_L, GPIO.HIGH)            #CWをOFFに
      time.sleep(waittime_L)
    for i in range(500,2000,2):
      GPIO.output(CWp_L, GPIO.HIGH)
      GPIO.output(CWm_L, GPIO.LOW)             #CWをONに
      time.sleep(waittime_L+(starttime/(2001-i)))
      GPIO.output(CWp_L, GPIO.LOW)
      GPIO.output(CWm_L, GPIO.HIGH)            #CWをOFFに
      time.sleep(waittime_L+(starttime/(2001-i)))
    
def left_B():   #左ステッピングモータを逆転させる関数
  while True:
    GPIO.output(CCWp_L, GPIO.HIGH)
    GPIO.output(CCWm_L, GPIO.LOW)             #CCWをONに
    time.sleep(waittime)
    GPIO.output(CCWp_L, GPIO.LOW)
    GPIO.output(CCWm_L, GPIO.HIGH)            #CCWをOFFに
    time.sleep(waittime)

def right_G():  #右ステッピングモータを正転させる関数
  while True:
    GPIO.output(7, GPIO.HIGH)
    GPIO.output(5, GPIO.LOW)             #CWをONに
    time.sleep(waittime)
    GPIO.output(7, GPIO.LOW)
    GPIO.output(5, GPIO.HIGH)            #CWをOFFに
    time.sleep(waittime)
    
def left_G():   #左ステッピングモータを正転させる関数
  while True:
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(12, GPIO.LOW)             #CWをONに
    #print("GPIO_HIGH")
    time.sleep(waittime)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(12, GPIO.HIGH)            #CWをOFFに
    #print("GPIO_LOW")
    time.sleep(waittime)    

try:
    if __name__ == "__main__":
        #thread_2 = threading.Thread(target=right_G)  #right_G  turn_R
        thread_1 = threading.Thread(target=right_G)  #left_G  turn_L
        
        #thread_2.start()
        thread_1.start()

except KeyboardInterrupt:       #Ctrl+Cキーが押された
        GPIO.cleanup()              #GPIOをクリーンアップ
        sys.exit()                  #プログラム終了
