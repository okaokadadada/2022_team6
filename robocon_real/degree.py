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
X=[0,0,0,0,0,0,0,0,0,0]
Y=[0,0,0,0,0,0,0,0,0,0]
Z=[0,0,0,0,0,0,0,0,0,0]
i=0

avX=0
avY=0
avZ=0



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

if __name__ == "__main__":
  
    while True:

        mag = mag_value()
        X[i]=mag[0]-25
        Y[i]=mag[1]+20
        Z[i]=mag[2] 
        i+=1
        if i==9:
            avX=0
            avY=0
            avZ=0
            for k in range(10):
                avX+=X[k]
                avY+=Y[k]
                avZ+=Z[k]
            
            i=0
            deg=0

            if avX>0 :
              deg=np.rad2deg(avY/avX)+86
            if avX<0 :
              deg=np.rad2deg(avY/avX)+266
            if avX==0 :
              deg=0
            print(deg)
       # print("Mag -> x:{}, y:{}, z: {}".format(mag[0], mag[1], mag[2]))
        
        time.sleep(0.1)

