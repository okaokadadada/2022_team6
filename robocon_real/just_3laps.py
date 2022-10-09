from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

#超音波センサのピン設定
Trig_F = 27                           
Echo_F = 18                           
Trig_L =                            
Echo_L =                            

#モータのピン設定
CWp_R=17
CWm_R=3
CCWp_R=5
CCWm_R=6
CWp_L=
CWm_L=
CCWp_L=
CCWm_L=

#モータのピン設定
GPIO.setmode(GPIO.BCM)               #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(CWp_R, GPIO.OUT)            #GPIO17を出力モードに設定
GPIO.setup(CWm_R, GPIO.OUT)            #GPIO3を出力モードに設定
GPIO.setup(CCWp_R, GPIO.OUT)           #GPIO23を出力モードに設定
GPIO.setup(CCWm_R, GPIO.OUT)           #GPIO4を出力モードに設定
GPIO.setup(CWp_L, GPIO.OUT)            #GPIO17を出力モードに設定
GPIO.setup(CWm_L, GPIO.OUT)            #GPIO3を出力モードに設定
GPIO.setup(CCWp_L, GPIO.OUT)           #GPIO23を出力モードに設定
GPIO.setup(CCWm_L, GPIO.OUT)           #GPIO4を出力モードに設定

　#超音波センサ
GPIO.setup(Trig_F, GPIO.OUT)          #GPIO27を出力モードに設定
GPIO.setup(Echo_F, GPIO.IN)           #GPIO18を入力モードに設定
GPIO.setup(Trig_L, GPIO.OUT)          #GPIO27を出力モードに設定
GPIO.setup(Echo_L, GPIO.IN)           #GPIO18を入力モードに設定

#HC-SR04で距離を測定する関数
#前方
def read_distance_F():

    global sig_on_F
    global sig_off_F

    GPIO.output(Trig_F, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
    time.sleep(0.00001)                     #10μ秒間待つ
    GPIO.output(Trig_F, GPIO.LOW)             #GPIO27の出力をLow(0V)にする

    while GPIO.input(Echo_F) == GPIO.LOW:     #GPIO18がLowの時間
        sig_off_F = time.time()
    while GPIO.input(Echo_F) == GPIO.HIGH:    #GPIO18がHighの時間
        sig_on_F = time.time()

    duration = sig_off_F - sig_on_F             #GPIO18がHighしている時間を算術
    distance_F = duration_F * 34000 / 2         #距離を求める(cm)
    return distance_F

#左方
def read_distance_L():

    global sig_on_L
    global sig_off_L

    GPIO.output(Trig_L, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
    time.sleep(0.00001)                     #10μ秒間待つ
    GPIO.output(Trig_L, GPIO.LOW)             #GPIO27の出力をLow(0V)にする

    while GPIO.input(Echo_L) == GPIO.LOW:     #GPIO18がLowの時間
        sig_off_L = time.time()
    while GPIO.input(Echo_L) == GPIO.HIGH:    #GPIO18がHighの時間
        sig_on_L = time.time()

    duration = sig_off_L - sig_on_L             #GPIO18がHighしている時間を算術
    distance_L = duration_L * 34000 / 2         #距離を求める(cm)
    return distance_L

#ステッピングモータを制御する関数
def right_G(waittime):　#右ステッピングモータを正転させる関数
  GPIO.output(CWp_R, GPIO.HIGH)
  GPIO.output(CWm_R, GPIO.LOW)             #CWをONに
  time.sleep(waittime)
  GPIO.output(CWp_R, GPIO.LOW)
  GPIO.output(CWm_R, GPIO.HIGH)            #CWをOFFに
  time.sleep(waittime)
  
def right_B(waittime):　#右ステッピングモータを逆転させる関数
  GPIO.output(CCWp_R, GPIO.HIGH)
  GPIO.output(CCWm_R, GPIO.LOW)             #CCWをONに
  time.sleep(waittime)
  GPIO.output(CCWp_R, GPIO.LOW)
  GPIO.output(CCWm_R, GPIO.HIGH)            #CCWをOFFに
  time.sleep(waittime)
    
def left_G(waittime):　#左ステッピングモータを正転させる関数
  GPIO.output(CWp_L, GPIO.HIGH)
  GPIO.output(CWm_L, GPIO.LOW)             #CWをONに
  time.sleep(waittime)
  GPIO.output(CWp_L, GPIO.LOW)
  GPIO.output(CWm_L, GPIO.HIGH)            #CWをOFFに
  time.sleep(waittime)
  
def left_B(waittime):　#左ステッピングモータを逆転させる関数
  GPIO.output(CCWp_L, GPIO.HIGH)
  GPIO.output(CCWm_L, GPIO.LOW)             #CCWをONに
  time.sleep(waittime)
  GPIO.output(CCWp_L, GPIO.LOW)
  GPIO.output(CCWm_L, GPIO.HIGH)            #CCWをOFFに
  time.sleep(waittime)
    
#旋回回数
turn = 0

#旋回を始める距離
distance_F = 

#左の壁との距離
distance_L = 

while turn<11:
  try:
        cm_F = -read_distance_F()
        print(cm_F)                   #HC-SR04で距離を測定する
        if cm > 2 and cm < 400:                #距離が2～400cmの場合
            print("distanceF=", int(cm_F), "cm")  #距離をint型で表示
        else:
            print("over")
        
        cm_L = -read_distance_L()
        print(cm_L)                   #HC-SR04で距離を測定する
        if cm > 2 and cm < 400:                #距離が2～400cmの場合
            print("distance_L=", int(cm_L), "cm")  #距離をint型で表示
        else:
            print("over")
        
        if cm_F<distance_F:           #前壁との距離が規定値未満になったら，旋回回数の値を＋１して右旋回
            right_G(0.003)
            left_G(0.001)

            turn = turn + 1
            print("turn=", int(turn))　#旋回回数をint型で表示
            
        if cm_F>=distance_F:          #前壁との距離が規定値以上になったら直進
            if cm_L<distance_L        #左壁との距離が規定値未満になったら右に方向修正
                right_G(0.002)
                left_G(0.001)
        　　　
            if cm_L>=distance_L       #左壁との距離が規定値以上になったら左に方向修正
                right_G(0.001)
                left_G(0.002)

    except KeyboardInterrupt:       #Ctrl+Cキーが押された
        GPIO.cleanup()              #GPIOをクリーンアップ
        sys.exit()                  #プログラム終了
