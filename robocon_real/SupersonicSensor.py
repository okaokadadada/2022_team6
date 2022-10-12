#必要なモジュールをインポート
from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート
import threading

#ポート番号の定義
Trig = 10                           #変数"Trig"に27を代入
Echo = 24                           #変数"Echo"に18を代入

sig_on = 0
sig_off = 0

#GPIOの設定
GPIO.setmode(GPIO.BCM)              #GPIOのモードを"GPIO.BCM"に設定
GPIO.setup(Trig, GPIO.OUT)          #GPIO27を出力モードに設定
GPIO.setup(Echo, GPIO.IN)           #GPIO18を入力モードに設定

#HC-SR04で距離を測定する関数
def read_distance():

    global sig_on
    global sig_off

    GPIO.output(Trig, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
    time.sleep(0.00001)                     #10μ秒間待つ
    GPIO.output(Trig, GPIO.LOW)             #GPIO27の出力をLow(0V)にする

    while GPIO.input(Echo) == GPIO.LOW:     #GPIO18がLowの時間
        sig_off = time.time()
    while GPIO.input(Echo) == GPIO.HIGH:    #GPIO18がHighの時間
        sig_on = time.time()


    duration = sig_off - sig_on             #GPIO18がHighしている時間を算術
    distance = duration * 34000 / 2         #距離を求める(cm)
    return distance

#連続して値を超音波センサの状態を読み取る
if __name__ == "__main__":
    thread_1 = threading.Thread(target=read_distance)
    thread_1.start()
#while True:
#    try:
#        cm = -read_distance()
#        print(cm)                   #HC-SR04で距離を測定する
#        if cm > 2 and cm < 400:                #距離が2～400cmの場合
#            print("distance=", int(cm), "cm")  #距離をint型で表示
#        # else:
#        #     print("over")
#        time.sleep(1)                          #1秒間待つ

#    except KeyboardInterrupt:       #Ctrl+Cキーが押された
#        GPIO.cleanup()              #GPIOをクリーンアップ
#        sys.exit()                  #プログラム終了
