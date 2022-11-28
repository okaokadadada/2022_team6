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
CWp_R=16
CWm_R=19
CCWp_R=20
CCWm_R=21
CWp_L=7
CWm_L=5
CCWp_L=6
CCWm_L=12

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
initial=0
rimit = 200000
sig_on_F = 0
sig_off_F = 0
sig_on_L = 0
sig_off_L = 0
duration_F = 0
duration_L = 0
distance_F = 0
distance_L = 0
distance_preF = 0
distance_preL = 0
distanceborder_F = 10
distanceborder_L = 20

#旋回回数
turn_number = 0
turn = False

#モータの速度
slow = 0.007
normal = 0.005
fast = 0.003
speedrate = 3

turn_R_speed = 0.0075
turn_L_speed = 0.005
turn_R_range = 250
turn_L_range = 375

#モータの制御に用いる変数，定数
certainty = 0
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
    global sig_on_F
    global sig_off_F
    global sig_on_L
    global sig_off_L
    global duration_F
    global duration_L
    global distance_F
    global distance_L
    global distance_preF
    global distance_preL
    global rimit
    global turn_number
    global turn
    global initial
    global certainty
    global update
    while True:
        if a>300 or b>300 or c>300 or d>300:  #リセット報告
            a=0
            b=0
            c=0
            d=0
            #print("reset")
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
        if distance_F - distance_preF > 100:
          distance_F = distance_preF + 20
        elif distance_F - distance_preF < -100:
          distance_F = distance_preF - 20
        time.sleep(0.01)

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
            if d>rimit:
                break
        if d>rimit:
            continue
        duration_L = sig_on_L - sig_off_L           #GPIO18がHighしている時間を算術
        distance_L = duration_L * 34000 / 2         #距離を求める(cm)
        if distance_L - distance_preL > 100:
          distance_L = distance_preL + 10
        elif distance_L - distance_preL < -100:
          distance_L = distance_preL - 10
        time.sleep(0.01)
        
        update = 1
        
        #if distance_F < distanceborder_F:
         # certainty = certainty + 1
        #else:
         # certainty = 0
        
        if turn:
          print(f"前＝ {distance_F:5.1f} cm 左＝ {distance_L:5.1f} cm turn_number= {turn_number}")
        else:
          print(f"前＝ {distance_F:5.1f} cm 左＝ {distance_L:5.1f}cm")
        
        if initial < 51:
          initial = initial + 1
        
        distance_preF = distance_F
        distance_preL = distance_L

#ステッピングモータを制御する関数
def straight(waittime):  #右ステッピングモータを正転させる関数
    for i in range(int(0.5/waittime)):
        GPIO.output(CWp_R, GPIO.HIGH)
        GPIO.output(CWm_R, GPIO.LOW)
        GPIO.output(CWp_L, GPIO.HIGH)
        GPIO.output(CWm_L, GPIO.LOW)
        time.sleep(waittime)
        GPIO.output(CWp_R, GPIO.LOW)
        GPIO.output(CWm_R, GPIO.HIGH)
        GPIO.output(CWp_L, GPIO.LOW)
        GPIO.output(CWm_L, GPIO.HIGH)
        time.sleep(waittime)
  
def turn_R(waittime):
    for i in range(int(0.5/waittime)):
        if i % speedrate == 0:
            GPIO.output(CWp_R, GPIO.HIGH)
            GPIO.output(CWm_R, GPIO.LOW)
        GPIO.output(CWp_L, GPIO.HIGH)
        GPIO.output(CWm_L, GPIO.LOW)
        time.sleep(waittime)
        if i % speedrate == 0:
            GPIO.output(CWp_R, GPIO.LOW)
            GPIO.output(CWm_R, GPIO.HIGH)
        GPIO.output(CWp_L, GPIO.LOW)
        GPIO.output(CWm_L, GPIO.HIGH)
        time.sleep(waittime)

def turn_L(waittime):
    for i in range(int(0.5/waittime)):
        GPIO.output(CWp_R, GPIO.HIGH)
        GPIO.output(CWm_R, GPIO.LOW)
        if i % speedrate == 0:
            GPIO.output(CWp_L, GPIO.HIGH)
            GPIO.output(CWm_L, GPIO.LOW)
        time.sleep(waittime)
        GPIO.output(CWp_R, GPIO.LOW)
        GPIO.output(CWm_R, GPIO.HIGH)
        if i % speedrate == 0:
            GPIO.output(CWp_L, GPIO.LOW)
            GPIO.output(CWm_L, GPIO.HIGH)
        time.sleep(waittime)

def back(waittime):  #右ステッピングモータを逆転させる関数
    for i in range(int(1/waittime)):
        GPIO.output(CCWp_R, GPIO.HIGH)
        GPIO.output(CCWm_R, GPIO.LOW)
        GPIO.output(CCWp_L, GPIO.HIGH)
        GPIO.output(CCWm_L, GPIO.LOW) 
        time.sleep(waittime)
        GPIO.output(CCWp_R, GPIO.LOW)
        GPIO.output(CCWm_R, GPIO.HIGH)
        GPIO.output(CCWp_L, GPIO.LOW)
        GPIO.output(CCWm_L, GPIO.HIGH)
        time.sleep(waittime)

def mortor():
    global turn_number
    global turn
    global update
    global distance_F
    global distance_L
    global distanceborder_F
    global distanceborder_L
    global fast
    global initial
    global speed_rate

    while True:
    update = 0
        if distance_F >= distanceborder_F:
            if distance_L < distanceborder_L:          #左壁との距離が規定値未満になったら右に方向修正
                turn_R(fast)
            elif distance_L > distanceborder_L + 20 and distance_L < 80:
                turn_L(fast)
            elif distance_L > distanceborder_L and distance_L < distanceborder_L + 20:
                straight(fast)
            else:
                back(fast)
                turn_L(fast)

try:
    if __name__ == "__main__":
        thread_1 = threading.Thread(target=read_distance)
        thread_2 = threading.Thread(target=mortor)

        thread_1.start()
        thread_2.start()

except KeyboardInterrupt:       #Ctrl+Cキーが押された
        GPIO.cleanup()              #GPIOをクリーンアップ
        sys.exit()                  #プログラム終了
