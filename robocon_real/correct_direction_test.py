from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート
import threading

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
distanceborder_F = 65
distanceborder_L = 20
distance = 10
danger = False
certainty = 0

#旋回回数
turn_number = 0
turn = False

# 左右のモータの回転数を記録
rotate_R = 0
rotate_L = 0

#モータの速度
slow = 0.007
normal = 0.005
fast = 0.003

turn_R_speed = 0.0075
turn_L_speed = 0.005
turn_R_range = 250
turn_L_range = 375

#モータの制御に用いる変数，定数
certainty = 0
A = 0
update = 0
last_move_R = 0
last_move_L = 0
slow_R = 1
normal_R = 2
fast_R = 3
slow_L = 1
normal_L = 2
fast_L = 3




def correct_direction(watetime):
    print("correct start")
    global rotate_R 
    global rotate_L
    rotate_ave = (rotate_R + rotate_L)/2 
    if rotate_R - rotate_ave > 0: # 右の方が多く回転している場合
        for i in range(int(abs(rotate_R - rotate_ave))):
            # 右逆転
            GPIO.output(CCWp_R, GPIO.HIGH)
            GPIO.output(CCWm_R, GPIO.LOW)
            # 左正転
            GPIO.output(CWp_L, GPIO.HIGH)
            GPIO.output(CWm_L, GPIO.LOW)

            time.sleep(watetime)

            # 右逆転
            GPIO.output(CCWp_R, GPIO.LOW)
            GPIO.output(CCWm_R, GPIO.HIGH)
            # 左正転
            GPIO.output(CWp_L, GPIO.LOW)
            GPIO.output(CWm_L, GPIO.HIGH)
            
            time.sleep(watetime)


    elif rotate_L - rotate_ave > 0: # 左の方が多く回転している場合
        for i in range(int(abs(rotate_R - rotate_ave))):
            # 右正転
            GPIO.output(CWp_R, GPIO.HIGH)
            GPIO.output(CWm_R, GPIO.LOW)
            # 左逆転
            GPIO.output(CCWp_L, GPIO.HIGH)  
            GPIO.output(CCWm_L, GPIO.LOW) 
            
            time.sleep(watetime)

            # 右正転
            GPIO.output(CWp_R, GPIO.LOW)
            GPIO.output(CWm_R, GPIO.HIGH)
            # 左逆転
            GPIO.output(CCWp_L, GPIO.LOW)
            GPIO.output(CCWm_L, GPIO.HIGH)
            
            time.sleep(watetime)

        
        rotate_R = 0
        rotate_l = 0
        
rotate_R = 50
rotate_L = 100
correct_direction(fast)
