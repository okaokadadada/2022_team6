#必要なモジュールをインポート
from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート
import threading

#ポート番号の定義
Trig_F = 23
Echo_F = 24
Trig_L = 14
Echo_L = 27


times = 0.00001
sleeps = 0.075

sig_on_F = 0
sig_off_F = 0
sig_on_L = 0
sig_off_L = 0
duration_F = 0
duration_L = 0
distance_F = 0
distance_L = 0
test_F1 = 0
test_F2 = 0
test_L1 = 0
test_L2 = 0
test_start = 0
test_finish = 0
rimit = 20000
a=0
b=0
c=0
d=0

#GPIOの設定
GPIO.setmode(GPIO.BCM)              #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(Trig_F, GPIO.OUT)          #GPIO27を出力モードに設定
GPIO.setup(Echo_F, GPIO.IN)           #GPIO18を入力モードに設定
GPIO.setup(Trig_L, GPIO.OUT)          #GPIO27を出力モードに設定
GPIO.setup(Echo_L, GPIO.IN)           #GPIO18を入力モードに設定

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
    global test_F1
    global test_F2
    global test_L1
    global test_L2
    global a
    global b
    global c
    global d

    while True:
        if a>rimit or b>rimit or c>rimit or d>rimit:
            if a>rimit:
              print("reset_a")
            if b>rimit:
              print("reset_b")
            if c>rimit:
              print("reset_a")
            if d>rimit:
              print("reset_b")
        a=0
        b=0
        c=0
        d=0
        GPIO.output(Trig_F, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
        time.sleep(times)                     #10μ秒間待つ
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

        duration_F = sig_on_F - sig_off_F             #GPIO18がHighしている時間を算術
        distance_F = duration_F * 34000 / 2         #距離を求める(cm)
        time.sleep(sleeps)                          #1秒間待つ


        GPIO.output(Trig_L, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
        time.sleep(times)                     #10μ秒間待つ
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

        duration_L = sig_on_L - sig_off_L             #GPIO18がHighしている時間を算術
        distance_L = duration_L * 34000 / 2         #距離を求める(cm)
        time.sleep(sleeps)                          #1秒間待つ

        print("前", f"{distance_F:.2f}", "cm", "左=", f"{distance_L:.2f}", "cm")  #距離をint型で表示

#連続して値を超音波センサの状態を読み取る

try:
    read_distance()    

except KeyboardInterrupt:       #Ctrl+Cキーが押された
    GPIO.cleanup()              #GPIOをクリーンアップ
    sys.exit()                  #プログラム終了
