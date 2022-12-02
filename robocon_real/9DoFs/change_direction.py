#$ sudo raspi-configでI2Cの設定
#P5 I2C Enable/disable・・・を＜Select＞してI2CをON
#rebootで再起動
#$ lsmodでI2Cが利用できるか確認．「i2c_bcm（4桁）」と表示されていることを確認．
#$ sudo i2cdetect -y 1でセンサのアドレスを確認．13,19,69になっているか確認
#$ sudo apt-get update
#↓
#$ sudo apt-get install i2c-tools python-smbus libi2c-devを入力し
#続行しますか？ [Y/n] でyを入力
# -*- coding: utf-8 -*-
from smbus import SMBus
import time
import math
import datetime
import csv
import numpy as np

# I2C
ACCL_ADDR = 0x19
ACCL_R_ADDR = 0x02
GYRO_ADDR = 0x69
GYRO_R_ADDR = 0x02
MAG_ADDR = 0x13
MAG_R_ADDR = 0x42
i2c = SMBus(1)

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
    print('avX='+str(avX))
    avY=np.average(y)
    print('avY='+str(avY))
    
    if avX>0 :
            now_direction=(np.rad2deg(math.atan(avY/avX)))%360
    if avX<0 :
            now_direction=(np.rad2deg(math.atan(avY/avX))+180)%360
    if avX==0 :
            now_direction=0
            
    difference=(now_direction-id)%360

    print(now_direction)

    if difference>20 and difference<180:
            print("R")
    if difference<340 and difference>180:
            print("L")
    
if __name__ == "__main__":
    bmx_setup()
    time.sleep(0.1)
    id=initial()
    while True:
        compass() 
        
