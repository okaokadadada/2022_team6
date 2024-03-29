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

def update():
    X=int((max_x+min_x)/2)
    Y=int((max_y+min_y)/2)

    print('center is ('+str(X)+','+str(Y)+')')
    


def compass():
    x=[0,0,0,0,0,0,0,0,0,0]
    y=[0,0,0,0,0,0,0,0,0,0]
    
    for i in range(10):
        mag=mag_value()
        print(mag)
        x[i]=mag[0]
        y[i]=mag[1]
       
        
        time.sleep(0.1)

    avX=np.average(x)
    avY=np.average(y)
    
    global max_x
    global min_x
    global max_y
    global min_y

    if max_x==None:
        max_x=avX  
    if min_x==None:
        min_x=avX
    if max_y==None:
        max_y=avY
    if min_y==None:
        min_y=avY

    if avX>max_x:
        max_x=avX
        update()
    if avX<min_x:
        min_x=avX
        update()
    if avY>max_y:
        max_y=avY
        update()
    if avY<min_y:
        min_y=avY
        update()
        
   
   
if __name__ == "__main__":
    bmx_setup()
    time.sleep(0.1)
    max_x=None
    min_x=None
    max_y=None
    min_y=None
    compass()
    while True:
        compass() 
