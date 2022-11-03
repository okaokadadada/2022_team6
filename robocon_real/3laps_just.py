from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート
import threading

#超音波センサのピン設定
Trig_F = 23
Echo_F = 24
Trig_L = 14
Echo_L = 27

#モータのGPIO設定
CWp_R=2
CWm_R=3
CCWp_R=4
CCWm_R=14
CWp_L=15
CWm_L=18
CCWp_L=17
CCWm_L=27

#モータのGPIO設定
GPIO.setmode(GPIO.BCM)               #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(CWp_R, GPIO.OUT)            #GPIO17を出力モードに設定
GPIO.setup(CWm_R, GPIO.OUT)            #GPIO3を出力モードに設定
GPIO.setup(CCWp_R, GPIO.OUT)           #GPIO23を出力モードに設定
GPIO.setup(CCWm_R, GPIO.OUT)           #GPIO4を出力モードに設定
GPIO.setup(CWp_L, GPIO.OUT)            #GPIO　を出力モードに設定
GPIO.setup(CWm_L, GPIO.OUT)            #GPIO　を出力モードに設定
GPIO.setup(CCWp_L, GPIO.OUT)           #GPIO　を出力モードに設定
GPIO.setup(CCWm_L, GPIO.OUT)           #GPIO　を出力モードに設定

#超音波センサのピン設定
GPIO.setup(Trig_F, GPIO.OUT)          #GPIO27を出力モードに設定
GPIO.setup(Echo_F, GPIO.IN)           #GPIO18を入力モードに設定
GPIO.setup(Trig_L, GPIO.OUT)          #GPIO27を出力モードに設定
GPIO.setup(Echo_L, GPIO.IN)           #GPIO18を入力モードに設定

#距離測定に使用する変数，定数
a=0
b=0
c=0
d=0
rimit = 600
sig_on_F = 0
sig_off_F = 0
sig_on_L = 0
sig_off_L = 0
duration_F = 0
duration_L = 0
distance_F = 30
distance_L = 30
distanceborder_F = 20
distanceborder_L = 20

#旋回回数
turn = 0

#モータの速度
  #遅い
slow = 0.01
  #普通
normal = 0.001
  #速い
fast = 0.0005

#モータの制御に用いる変数，定数
eR = 0
eL = 0
update = 0
last_move_R = 0
last_move_L = 0
slow_R = 1
normal_R = 2
fast_R = 3
slow_L = 1
normal_L = 2
fast_L = 3

#HC-SR04で距離を測定する関数
def read_distance():
    global a
    global b
    global c
    global d
    global update
    global rimit
    global sig_on_F
    global sig_off_F
    global sig_on_L
    global sig_off_L
    global duration_F
    global duration_L
    global distance_F
    global distance_L
    while True:
        if a>300 or b>300 or c>300 or d>300:  #リセット報告
            a=0
            b=0
            c=0
            d=0
            print("reset")
        a=0
        b=0
        c=0
        d=0
        #前方
        GPIO.output(Trig_F, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
        time.sleep(0.00001)                     #10μ秒間待つ
        GPIO.output(Trig_F, GPIO.LOW)             #GPIO27の出力をLow(0V)にする

        while GPIO.input(Echo_F) == GPIO.LOW:     #GPIO18がLowの時間
            sig_off_F = time.time()
            a=a+1
            if a>rimit:
                break
        if a>rimit:
            continue
        while GPIO.input(Echo_F) == GPIO.HIGH:    #GPIO18がHighの時間
            sig_on_F = time.time()
            b=b+1
            if b>rimit:
                break
        if b>rimit:
            continue
        duration_F = sig_on_F -sig_off_F            #GPIO18がHighしている時間を算術
        distance_F = duration_F * 34000 / 2         #距離を求める(cm)
        time.sleep(0.05)

        #左方
        GPIO.output(Trig_L, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
        time.sleep(0.00001)                     #10μ秒間待つ
        GPIO.output(Trig_L, GPIO.LOW)             #GPIO27の出力をLow(0V)にする

        while GPIO.input(Echo_L) == GPIO.LOW:     #GPIO18がLowの時間
            sig_off_L = time.time()
            c=c+1
            if c>rimit:
                break
        if c>rimit:
            continue
        while GPIO.input(Echo_L) == GPIO.HIGH:    #GPIO18がHighの時間
            sig_on_L = time.time()
            d=d+1
            if d>300:
                break
        if d>rimit:
            continue
        duration_L = sig_on_L - sig_off_L           #GPIO18がHighしている時間を算術
        distance_L = duration_L * 34000 / 2         #距離を求める(cm)
        time.sleep(0.05)
        
        #duration_F, duration_L, sig_on_F, sig_on_L, sig_off_F, sig_off_L, 
        update = 1
        print("前＝", f"{distance_F:.2f}", "cm", "左＝", f"{distance_L:.2f}", "cm")

#ステッピングモータを制御する関数
def right_G(waittime):  #右ステッピングモータを正転させる関数
  GPIO.output(CWp_R, GPIO.HIGH)
  GPIO.output(CWm_R, GPIO.LOW)             #CWをONに
  time.sleep(waittime)
  GPIO.output(CWp_R, GPIO.LOW)
  GPIO.output(CWm_R, GPIO.HIGH)            #CWをOFFに
  time.sleep(waittime)
  
def right_B(waittime):  #右ステッピングモータを逆転させる関数
  GPIO.output(CCWp_R, GPIO.HIGH)
  GPIO.output(CCWm_R, GPIO.LOW)             #CCWをONに
  time.sleep(waittime)
  GPIO.output(CCWp_R, GPIO.LOW)
  GPIO.output(CCWm_R, GPIO.HIGH)            #CCWをOFFに
  time.sleep(waittime)
    
def left_G(waittime):   #左ステッピングモータを正転させる関数
  GPIO.output(CWp_L, GPIO.HIGH)
  GPIO.output(CWm_L, GPIO.LOW)             #CWをONに
  time.sleep(waittime)
  GPIO.output(CWp_L, GPIO.LOW)
  GPIO.output(CWm_L, GPIO.HIGH)            #CWをOFFに
  time.sleep(waittime)
  
def left_B(waittime):   #左ステッピングモータを逆転させる関数
  GPIO.output(CCWp_L, GPIO.HIGH)
  GPIO.output(CCWm_L, GPIO.LOW)             #CCWをONに
  time.sleep(waittime)
  GPIO.output(CCWp_L, GPIO.LOW)
  GPIO.output(CCWm_L, GPIO.HIGH)            #CCWをOFFに
  time.sleep(waittime)

def turn_R():
    for i in range(100):
        GPIO.output(CWp_R, GPIO.HIGH)
        GPIO.output(CWm_R, GPIO.LOW)             #CWをONに
        time.sleep(0.03)
        GPIO.output(CWp_R, GPIO.LOW)
        GPIO.output(CWm_R, GPIO.HIGH)            #CWをOFFに
        time.sleep(0.03)
    

def turn_L():
    global turn
    turn = turn + 1
    for i in range(100):
        GPIO.output(CWp_L, GPIO.HIGH)
        GPIO.output(CWm_L, GPIO.LOW)             #CWをONに
        time.sleep(0.03)
        GPIO.output(CWp_L, GPIO.LOW)
        GPIO.output(CWm_L, GPIO.HIGH)            #CWをOFFに
        time.sleep(0.03)
        print("turn=", int(turn))  #旋回回数をint型で表示
    
    
def mortor_R():
    global turn
    global eR
    global update
    global distance_F
    global distance_L
    global distanceborder_F
    global distanceborder_L
    global slow
    global normal
    global fast
    global slow_R
    global normal_R
    global fast_R
    global last_move_R
    
    while True:
      update = 0
      if turn<11:
        if distance_F < distanceborder_F:             #前壁との距離が規定値未満になったら，旋回回数の値を＋１して右旋回
          eR = eR + 1 
          if last_move_R == slow_R:
            while update == 0:
                right_G(slow)
                print("                SLOW_R")
          if last_move_R == normal_R:
            while update == 0:
                right_G(normal)
                print("                NORMAL_L")
          if last_move_R == fast_R:
            while update == 0:
                right_G(fast)
                print("                FAST_L")
          if eR > 3:
            turn_R()

        if distance_F >= distanceborder_F:            #前壁との距離が規定値以上になったら直進
            eR = 0
            if distance_L < distanceborder_L:          #左壁との距離が規定値未満になったら右に方向修正
              while update == 0:
                  right_G(slow)
                  print("                SLOW_R")
              last_move_L = slow_L

            elif distance_L >= distanceborder_L+20:    #左壁との距離が規定値以上になったら左に方向修正
              while update == 0:
                  right_G(fast)
                  print("                FAST_R")
              last_move_L = fast_L

            else:
              while update == 0:
                  right_G(normal)
                  print("                NAOMAL_R")
              last_move_R = normal_R


def mortor_L():
    global turn
    global eL
    global update
    global distance_F
    global distance_L
    global distanceborder_F
    global distanceborder_L
    global slow
    global normal
    global fast
    global slow_L
    global normal_L
    global fast_L
    global last_move_L
    
    while True:
        update = 0
        if turn<11:
          if distance_F < distanceborder_F:             #前壁との距離が規定値未満になったら，旋回回数の値を＋１して右旋回
            eL = eL + 1
            if last_move_L == slow_L:
                while update == 0:
                    left_G(slow)
                    print("                SLOW_L")
            if last_move_L == normal_L:
                while update == 0:
                    left_G(normal)
                    print("                NORMAL_L")
            if last_move_L == fast_L:
                while update == 0:
                    left_G(fast)
                    print("                FAST_L")
            if eL > 3:
                turn_L()

          if distance_F >= distanceborder_F:            #前壁との距離が規定値以上になったら直進
            eL=0
            if distance_L < distanceborder_L:          #左壁との距離が規定値未満になったら右に方向修正
              while update == 0:
                  left_G(fast)
                  print("                FAST_L")
              last_move_L = fast_L

            elif distance_L >= distanceborder_L+20:    #左壁との距離が規定値以上になったら左に方向修正
              while update == 0:
                  left_G(slow)
                  print("                SLOW_L")
              last_move_L = slow_L

            else:
              while update == 0:
                  left_G(normal)
                  print("                NORMAL_L")
              last_move_L = normal_L

try:
    if __name__ == "__main__":
        thread_1 = threading.Thread(target=read_distance)
        thread_2 = threading.Thread(target=mortor_R)
        thread_3 = threading.Thread(target=mortor_L)

        thread_1.start()
        thread_2.start()
        thread_3.start()

except KeyboardInterrupt:       #Ctrl+Cキーが押された
        GPIO.cleanup()              #GPIOをクリーンアップ
        sys.exit()                  #プログラム終了
