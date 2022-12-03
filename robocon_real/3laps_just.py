from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

from smbus import SMBus
import time
import math
import datetime
import csv
import numpy as np

#超音波センサのピン設定
Trig_F = 17
Echo_F = 15
Trig_LF = 14
Echo_LF = 27
Trig_LB = 23
Echo_LB = 24

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
GPIO.setup(Trig_LF, GPIO.OUT)          #GPIO27を出力モードに設定
GPIO.setup(Echo_LF, GPIO.IN)           #GPIO18を入力モードに設定
GPIO.setup(Trig_LB, GPIO.OUT)          #GPIO27を出力モードに設定
GPIO.setup(Echo_LB, GPIO.IN)           #GPIO18を入力モードに設定

#距離測定に使用する変数，定数
a = 0
b = 0
c = 0
d = 0
e = 0
f = 0
n = 0
rimit = 2000
sig_on_F = 0
sig_off_F = 0
duration_F = 0
distance_F = 0
sig_on_LF = 0
sig_off_LF = 0
duration_LF = 0
distance_LF = 0
sig_on_LB = 0
sig_off_LB = 0
duration_LB = 0
distance_LB = 0
distanceborder_F = 65
distanceborder_F_short = 100
distanceborder_LF = 40

# 左右のモータの回転数を記録
rotate_R = 0
rotate_L = 0

#旋回回数
turn_number = 0
turn = False

#モータの速度
fast = 0.006

rate_R = 10
rate_L = 10

#9軸センサに用いる変数，定数
# I2C
ACCL_ADDR = 0x19
ACCL_R_ADDR = 0x02
GYRO_ADDR = 0x69
GYRO_R_ADDR = 0x02
MAG_ADDR = 0x13
MAG_R_ADDR = 0x42
i2c = SMBus(1)
    
#ステッピングモータを制御する関数
def straight(waittime,repeat):  #右ステッピングモータを正転させる関数
    print("straight")
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

def roll(waittime,repeat,rate_rollR,rate_rollR):  #右ステッピングモータを正転させる関数
    print("roll")
    for i in range(int(repeat)):
        if i % rate_rollR == 0 and i % rate_rollL == 0:
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
        elif i % rate_rollR == 0:
            GPIO.output(CWp_R, GPIO.HIGH)
            GPIO.output(CWm_R, GPIO.LOW)
            time.sleep(waittime)
            GPIO.output(CWp_R, GPIO.LOW)
            GPIO.output(CWm_R, GPIO.HIGH)
            time.sleep(waittime)
        elif i % rate_rollL == 0:
            GPIO.output(CWp_L, GPIO.HIGH)
            GPIO.output(CWm_L, GPIO.LOW)
            time.sleep(waittime)
            GPIO.output(CWp_L, GPIO.LOW)
            GPIO.output(CWm_L, GPIO.HIGH)
            time.sleep(waittime)
        
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

# 9軸センサの関数-------------------------------------------------------------------------
def bmx_setup():
    # mag_data_setup : 地磁気値をセットアップ
    data = i2c.read_byte_data(MAG_ADDR, 0x4B)
    if(data == 0):
        i2c.write_byte_data(MAG_ADDR, 0x4B, 0x83)
        time.sleep(0.5)
    i2c.write_byte_data(MAG_ADDR, 0x4B, 0x01)
    i2c.write_byte_data(MAG_ADDR, 0x4C, 0x00)
    i2c.write_byte_data(MAG_ADDR, 0x4E, 0x84)
    i2c.write_byte_data(MAG_ADDR, 0x51, 0x04)
    i2c.write_byte_data(MAG_ADDR, 0x52, 0x16)
    time.sleep(0.5)
    
def mag_value():
    data = [0, 0, 0, 0, 0, 0, 0, 0]
    mag_data = [0.0, 0.0, 0.0]
    try:
        for i in range(8):
            data[i] = i2c.read_byte_data(MAG_ADDR, MAG_R_ADDR + i)
        for i in range(3):
            if i != 2:
                mag_data[i] = ((data[2*i + 1] * 256) + (data[2*i] & 0xF8)) / 8
                if mag_data[i] > 4095:
                    mag_data[i] -= 8192
            else:
                mag_data[i] = ((data[2*i + 1] * 256) + (data[2*i] & 0xFE)) / 2
                if mag_data[i] > 16383:
                    mag_data[i] -= 32768
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    return mag_data

def initial():
    
    mag=mag_value()
    x=mag[0]+26
    y=mag[1]+90
    if x>0 :
        initial_direction=(np.rad2deg(math.atan(y/x)))%360
    if x<0 :
        initial_direction=(np.rad2deg(math.atan(y/x))+180)%360
    if x==0 :
        initial_direction=0

    print('initial_direction is'+str(initial_direction))
    return initial_direction

def compass():
    x=[0,0,0,0,0,0,0,0,0,0]
    y=[0,0,0,0,0,0,0,0,0,0]

    for i in range(10):
        mag=mag_value()
        x[i]=mag[0]+26
        y[i]=mag[1]+90
        
        time.sleep(0.1)

    avX=np.average(x)
#     print('avX='+str(avX))
    avY=np.average(y)
#     print('avY='+str(avY))
    
#     ベクトル → 角度
    if avX>0 :
            now_direction=(np.rad2deg(math.atan(avY/avX)))%360
    if avX<0 :
            now_direction=(np.rad2deg(math.atan(avY/avX))+180)%360
    if avX==0 :
            now_direction=0
            
    difference=now_direction-id

#     print(now_direction)

    if difference > 180:
      difference -= 360
    if difference < -180:
      difference += 360

    return difference

# ------------------------------------------------------------------------------------------------------
            
try:
    # 9軸のセットアップ
    bmx_setup()
    time.sleep(0.1)
    id=initial()
    
    while True:
        #超音波センサで距離を計測
        reset_F = 0
        distance_sumF = 0
        reset_LF = 0
        distance_sumLF = 0
        reset_LB = 0
        distance_sumLB = 0
        counter = 0
        distance_F_list = []
        distance_LF_list = []
        distance_LB_list = []
        
        while len(distance_F_list) < 10:
            if a>=rimit or b>=rimit :
                reset_F += 1
                #print("reset_F=",reset_F)
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
            distance_F_list.append(distance_F)
            time.sleep(0.001)

            #左方
        while len(distance_LF_list) < 10:
            if c>=rimit or d>=rimit :
                reset_LF += 1
                #print("reset_LF=",reset_LF)
            c=0
            d=0
            GPIO.output(Trig_LF, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
            time.sleep(0.00001)                     #10μ秒間待つ
            GPIO.output(Trig_LF, GPIO.LOW)             #GPIO27の出力をLow(0V)にする
            while GPIO.input(Echo_LF) == GPIO.LOW:     #GPIO18がLowの時間
                sig_off_LF = time.time()
                c=c+1
                if c>rimit:
                    break
            if c>rimit:
                continue
            while GPIO.input(Echo_LF) == GPIO.HIGH:    #GPIO18がHighの時間
                sig_on_LF = time.time()
                d=d+1
                if d>rimit:
                    break
            if d>rimit:
                continue
            duration_LF = sig_on_LF - sig_off_LF           #GPIO18がHighしている時間を算術
            distance_LF = duration_LF * 34000 / 2         #距離を求める(cm)
            distance_LF_list.append(distance_LF)
            time.sleep(0.001)
            
        #while len(distance_LB_list) < 10:
        #    if c>=rimit or d>=rimit :
        #        reset_LB += 1
        #        #print("reset_LB=",reset_LB)
        #    e=0
        #    f=0
        #    GPIO.output(Trig_LB, GPIO.HIGH)            #GPIO27の出力をHigh(3.3V)にする
        #    time.sleep(0.00001)                     #10μ秒間待つ
        #    GPIO.output(Trig_LB, GPIO.LOW)             #GPIO27の出力をLow(0V)にする
        #    while GPIO.input(Echo_LB) == GPIO.LOW:     #GPIO18がLowの時間
        #        sig_off_LB = time.time()
        #        e=e+1
        #        if e>rimit:
        #            break
        #    if e>rimit:
        #        continue
        #    while GPIO.input(Echo_LB) == GPIO.HIGH:    #GPIO18がHighの時間
        #        sig_on_LB = time.time()
        #        f=f+1
        #        if f>rimit:
        #            break
        #    if f>rimit:
        #        continue
        #    duration_LB = sig_on_LB - sig_off_LB           #GPIO18がHighしている時間を算術
        #    distance_LB = duration_LB * 34000 / 2         #距離を求める(cm)
        #    distance_LB_list.append(distance_LB)
        #    time.sleep(0.001)         
        
        #if reset_F == 10 or reset_LF == 10 or reset_LB == 10:
        #    counter += 1
        #    print(counter)
        #    continue
        
        for i in range(10):
            distance_sumF += distance_F_list[i]
            distance_sumLF += distance_LF_list[i]
            #distance_sum_LB += distance_LB_list[i]
        
        distance_F = distance_sumF / 10
        distance_LF = distance_sumLF / 10
        #distance_LB = distance_sumLB / 10

        print(f"前＝ {distance_F:5.1f} cm   左＝ {distance_LF:5.1f}cm")#   左後＝ {distance_LB:5.1f} cm")

        #モータの制御
        if distance_F < distanceborder_F:
            turn_number +=  1
            for i in range(3):
                difference = compass()
                print(f" difference = {difference}")
                if difference > 0:
                    turn_L(fast,int(abs(difference)),2)
                if difference < 0:
                    turn_R(fast,int(abs(difference)),2)
            print(f"旋回{turn_number}回目")
            #turn_R(fast,320,5)
            
            if turn_number == 11:
                print("break")
                break
            rotate_R = 0
            rotate_L = 0
            bmx_setup()
            time.sleep(0.1)
            id=initial()

        else:
            if distance_LF < distanceborder_LF:         #左壁との距離が規定値未満になったら右に方向修正
                turn_R(fast,50,2)
                straight(fast,400)
                
                difference = compass()
                print(f" difference = {difference}")
                if difference > 0:
                    turn_L(fast,int(abs(difference)),2)
                if difference < 0:
                    turn_R(fast,int(abs(difference)),2)
                
#                 correct_direction(fast)

            elif distance_LF > distanceborder_LF + 20:
                turn_L(fast,50,2)
                straight(fast,400)
                
                difference = compass()
                print(f" difference = {difference}")
                if difference > 0:
                    turn_L(fast,int(abs(difference)),2)
                if difference < 0:
                    turn_R(fast,int(abs(difference)),2)
                

#                 correct_direction(fast)

            else:
                if distance_F > distanceborder_F_short:
                    straight(fast, 1500)
                else:
                    straight(fast, 500)
                    
                if n > 2:
                    difference = compass()
                    print(f" difference = {difference}")
                    if difference > 0:
                        turn_L(fast,int(abs(difference)*1.2),2)
                    if difference < 0:
                        turn_R(fast,int(abs(difference)*1.2),2)
                    n = 0
                else:
                    n += 1
                    
            

except KeyboardInterrupt:       #Ctrl+Cキーが押された
        GPIO.cleanup()              #GPIOをクリーンアップ
        sys.exit()                  #プログラム終了
