from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート
import threading

#超音波センサのピン設定
Trig_F = 22
Echo_F = 23
Trig_L = 10
Echo_L = 24

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

#距離測定に使用する変数
a=0
b=0
c=0
d=0
sig_on_F = 0
sig_off_F = 0
sig_on_L = 0
sig_off_L = 0
duration_F = 0
duration_L = 0
distance_F = 30
distance_L = 0
distanceborder_F = 20
distanceborder_L = 20

#旋回回数
turn = 0

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
            if a>300:
                break
        if a>300:
            continue
        while GPIO.input(Echo_F) == GPIO.HIGH:    #GPIO18がHighの時間
            sig_on_F = time.time()
            b=b+1
            if b>300:
                break
        if b>300:
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
            if c>300:
                break
        if c>300:
            continue
        while GPIO.input(Echo_L) == GPIO.HIGH:    #GPIO18がHighの時間
            sig_on_L = time.time()
            d=d+1
            if d>300:
                break
        if d>300:
            continue
        duration_L = sig_on_L - sig_off_L           #GPIO18がHighしている時間を算術
        distance_L = duration_L * 34000 / 2         #距離を求める(cm)
        time.sleep(0.05)
        
        #duration_F, duration_L, sig_on_F, sig_on_L, sig_off_F, sig_off_L, 
        print("前=", distance_F, "  左=", distance_L)

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
    for i in range(500):
        GPIO.output(CWp_R, GPIO.HIGH)
        GPIO.output(CWm_R, GPIO.LOW)             #CWをONに
        time.sleep(0.03)
        GPIO.output(CWp_R, GPIO.LOW)
        GPIO.output(CWm_R, GPIO.HIGH)            #CWをOFFに
        time.sleep(0.03)
    

def turn_L():
    global turn
    turn = turn + 1
    for i in range(3000):
        GPIO.output(CWp_L, GPIO.HIGH)
        GPIO.output(CWm_L, GPIO.LOW)             #CWをONに
        time.sleep(0.005)
        GPIO.output(CWp_L, GPIO.LOW)
        GPIO.output(CWm_L, GPIO.HIGH)            #CWをOFFに
        time.sleep(0.005)
        print("                                     turn=", int(turn))  #旋回回数をint型で表示
    
    
def mortor_R():
    global turn
    global distance_F
    global distance_L
    global distanceborder_F
    global distanceborder_L
    while True:
        if turn<11:
            if distance_F<distanceborder_F:             #前壁との距離が規定値未満になったら，旋回回数の値を＋１して右旋回
                    turn_R()

            if distance_F>=distanceborder_F:            #前壁との距離が規定値以上になったら直進
                if distance_L<distanceborder_L:          #左壁との距離が規定値未満になったら右に方向修正
                    right_G(0.0065)

                elif distance_L>=distanceborder_L+10:    #左壁との距離が規定値以上になったら左に方向修正
                    right_G(0.0035)

                else:
                    right_G(0.005)


def mortor_L():
    global turn
    global distance_F
    global distance_L
    global distanceborder_F
    global distanceborder_L
    while True:
        if turn<11:
            if distance_F<distanceborder_F:             #前壁との距離が規定値未満になったら，旋回回数の値を＋１して右旋回
                    turn_L()

            if distance_F>=distanceborder_F:            #前壁との距離が規定値以上になったら直進
                if distance_L<distanceborder_L:          #左壁との距離が規定値未満になったら右に方向修正
                    left_G(0.0005)

                elif distance_L>=distanceborder_L+20:    #左壁との距離が規定値以上になったら左に方向修正
                    left_G(0.01)

                else:
                    left_G(0.001)

try:
    if __name__ == "__main__":
        #thread_1 = threading.Thread(target=read_distance)
        #thread_2 = threading.Thread(target=mortor_R)
        thread_3 = threading.Thread(target=mortor_L)

        #thread_1.start()
        #thread_2.start()
        thread_3.start()

except KeyboardInterrupt:       #Ctrl+Cキーが押された
        GPIO.cleanup()              #GPIOをクリーンアップ
        sys.exit()                  #プログラム終了
