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
a = 0
b = 0
c = 0
d = 0
rimit = 2000
sig_on_F = 0
sig_off_F = 0
sig_on_L = 0
sig_off_L = 0
duration_F = 0
duration_L = 0
distance_F = 0
distance_L = 0
distance_sumF = 0
distance_sumL = 0
distanceborder_F = 65
distanceborder_L = 20
distance = 20

# 左右のモータの回転数を記録
rotate_R = 0
rotate_L = 0

#旋回回数
turn_number = 0
turn = False

#モータの速度
slow = 0.007
normal = 0.005
fast = 0.006

rate_R = 10
rate_L = 11
    
#ステッピングモータを制御する関数
def straight(waittime,repeat):  #右ステッピングモータを正転させる関数
    print("straight")
    a=0
    b=0
    for i in range(int(repeat)):
        if i % rate_R == 0 and i % rate_L == 0:
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
        elif i % rate_R == 0:
            GPIO.output(CWp_R, GPIO.HIGH)
            GPIO.output(CWm_R, GPIO.LOW)
            time.sleep(waittime)
            GPIO.output(CWp_R, GPIO.LOW)
            GPIO.output(CWm_R, GPIO.HIGH)
            time.sleep(waittime)
        elif i % rate_L == 0:
            GPIO.output(CWp_L, GPIO.HIGH)
            GPIO.output(CWm_L, GPIO.LOW)
            time.sleep(waittime)
            GPIO.output(CWp_L, GPIO.LOW)
            GPIO.output(CWm_L, GPIO.HIGH)
            time.sleep(waittime)
  
def turn_R(waittime,repeat,speedrate):
    print("turnR")
    global rotate_R
    global rotate_L
    for i in range(repeat):
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

    rotate_R += int(repeat/speedrate)
    rotate_L += repeat

def turn_L(waittime,repeat,speedrate):
    print("turnL")
    global rotate_R
    global rotate_L
    for i in range(repeat):
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

    rotate_R += repeat
    rotate_L += int(repeat/speedrate)

def back(waittime):  #右ステッピングモータを逆転させる関数
    for i in range(150):
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

def correct_direction(waittime):
    global rotate_R 
    global rotate_L
    rotate_ave = (rotate_R + rotate_L)/2 
    print(f"correct_direction  rotate_ave＝　{rotate_R - rotate_ave}")
    if rotate_R - rotate_ave > 0: # 右の方が多く回転している場合
        for i in range(int(abs(rotate_R - rotate_ave)* 1.2)):
            # 右逆転
            GPIO.output(CCWp_R, GPIO.HIGH)
            GPIO.output(CCWm_R, GPIO.LOW)
            # 左正転
            GPIO.output(CWp_L, GPIO.HIGH)
            GPIO.output(CWm_L, GPIO.LOW)

            time.sleep(waittime)

            # 右逆転
            GPIO.output(CCWp_R, GPIO.LOW)
            GPIO.output(CCWm_R, GPIO.HIGH)
            # 左正転
            GPIO.output(CWp_L, GPIO.LOW)
            GPIO.output(CWm_L, GPIO.HIGH)
            
            time.sleep(waittime)


    elif rotate_L - rotate_ave > 0: # 左の方が多く回転している場合
        for i in range(int(abs(rotate_R - rotate_ave)* 3.1)):
            # 右正転
            GPIO.output(CWp_R, GPIO.HIGH)
            GPIO.output(CWm_R, GPIO.LOW)
            # 左逆転
            GPIO.output(CCWp_L, GPIO.HIGH)  
            GPIO.output(CCWm_L, GPIO.LOW) 
            
            time.sleep(waittime)

            # 右正転
            GPIO.output(CWp_R, GPIO.LOW)
            GPIO.output(CWm_R, GPIO.HIGH)
            # 左逆転
            GPIO.output(CCWp_L, GPIO.LOW)
            GPIO.output(CCWm_L, GPIO.HIGH)
            
            time.sleep(waittime)

    rotate_R = 0
    rotate_L = 0
            
            
try:
    while True:
        #超音波センサで距離を計測
        reset_F = 0
        reset_L = 0
        distance_sumF = 0
        distance_sumL = 0
        for i in range(10):
            if a>=rimit or b>=rimit :
                #print("resetAB")
                reset_F += 1
            a=0
            b=0
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
            distance_sumF += distance_F 
            time.sleep(0.001)

            #左方
        for i in range(10):
            if c>=rimit or d>=rimit :
                #print("reseCDt")
                reset_L += 1
            c=0
            d=0
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
            distance_sumL += distance_L
            time.sleep(0.001)            
            
            #print(f"i＝　{i}  前＝ {distance_F:5.1f} cm   左＝ {distance_L:5.1f}cm")
        if reset_F == 10 or reset_L == 10:
            continue
        distance_F = distance_sumF / (10 - reset_F)
        distance_L = distance_sumL / (10 - reset_L)

        if turn:
          print(f"前＝ {distance_F:5.1f} cm   左＝ {distance_L:5.1f} cm   turn_number= {turn_number}")
        else:
          print(f"前＝ {distance_F:5.1f} cm   左＝ {distance_L:5.1f}cm   difference＝{distance_F - distance_L:5.1f}")

        #モータの制御
        difference = distance_F - distance_L
        if abs(distance_F) < 50 and abs(distance_L) < 50:
            if difference >= 3:
                turn_L(fast,30,2)
            elif difference <= -3:
                turn_R(fast,30,2)
            else:
                straight(fast,1000)

except KeyboardInterrupt:       #Ctrl+Cキーが押された
        GPIO.cleanup()              #GPIOをクリーンアップ
        sys.exit()                  #プログラム終了
