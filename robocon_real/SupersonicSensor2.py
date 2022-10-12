import RPi.GPIO as GPIO
import time

#測定環境温度
TEMP = 20

#GPIO設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(24, GPIO.IN)

#繰り返し
while True:
    
    #トリガ信号出力
    GPIO.output(10, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(10, GPIO.LOW)
    
    #返送HIGHレベル時間計測
    while GPIO.input(24) == GPIO.LOW:
        soff = time.time()    #LOWレベル終了時刻
    
    while GPIO.input(24) == GPIO.HIGH:
        son = time.time()    #HIGHレベル終了時刻
    
    #時間から距離に変換(TEMPは測定環境温度)
    clc = (son - soff) * (331.50 + (0.6 * TEMP)) / 2 * 100
    
    #画面に表示
    print(clc, "cm")
    
    #一時停止
    time.sleep(0.1)
