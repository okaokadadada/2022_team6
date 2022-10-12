#必要なモジュールをインポート
from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート
import threading

#ポート番号の定義
Trig_F = 22
Echo_F = 23
Trig_L = 10
Echo_L = 24

sig_on_F
sig_off_F
sig_on_L
sig_off_L
duration_F
duration_L
distance_F
distance_L

#GPIOの設定
GPIO.setmode(GPIO.BCM)              #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(Trig, GPIO.OUT)          #GPIO27を出力モードに設定
GPIO.setup(Echo, GPIO.IN)           #GPIO18を入力モードに設定

#HC-SR04で距離を測定する関数
def read_distance():
    global sig_on_F
    global sig_off_F
    global sig_on_L
    global sig_off_L
    global duration_F
    global duration_L
    global distance_F
    global distance_L

    GPIO.output(Trig_F, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
    time.sleep(0.00001)                     #10μ秒間待つ
    GPIO.output(Trig_F, GPIO.LOW)             #GPIO27の出力をLow(0V)にする

    while GPIO.input(Echo_F) == GPIO.LOW:     #GPIO18がLowの時間
        sig_off_F = time.time()
    while GPIO.input(Echo_F) == GPIO.HIGH:    #GPIO18がHighの時間
        sig_on_F = time.time()

    duration_F = sig_on_F - sig_off_F             #GPIO18がHighしている時間を算術
    distance_F = duration_F * 34000 / 2         #距離を求める(cm)
    
    
    GPIO.output(Trig_L, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
    time.sleep(0.00001)                     #10μ秒間待つ
    GPIO.output(Trig_L, GPIO.LOW)             #GPIO27の出力をLow(0V)にする

    while GPIO.input(Echo_L) == GPIO.LOW:     #GPIO18がLowの時間
        sig_off_L = time.time()
    while GPIO.input(Echo_L) == GPIO.HIGH:    #GPIO18がHighの時間
        sig_on_L = time.time()

    duration_L = sig_on_L - sig_off_L             #GPIO18がHighしている時間を算術
    distance_L = duration_L * 34000 / 2         #距離を求める(cm)

#連続して値を超音波センサの状態を読み取る
while True:
    try:
        read_distance()
        print("duration_F=", duration_F, "duration_L=", duration_L)                   #HC-SR04で距離を測定する
        if cm > 2 and cm < 400:                #距離が2～400cmの場合
            print("distance_F=", distance_F, "cm", "distance_L=", distance_F, "cm")  #距離をint型で表示
        else:
            print("over")
        time.sleep(1)                          #1秒間待つ

    except KeyboardInterrupt:       #Ctrl+Cキーが押された
        GPIO.cleanup()              #GPIOをクリーンアップ
        sys.exit()                  #プログラム終了
