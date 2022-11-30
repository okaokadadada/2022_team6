import picamera #カメラモジュール用
import cv2
import numpy as np
import sys

cap = picamera.PiCamera() #インスタンス生成
cap.resolution = (1920, 1080) #画像サイズの指定
cap.capture("capture.jpg") #撮影

#処理する画像の名前
name="capture"
img = cv2.imread(name+".jpg")#読み込み

#2値化する
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = (75,0, 0)
upper = (250, 255, 255)
img2 = cv2.inRange(hsv, lower, upper)
cv2.imwrite(name+"_binarized.jpg",img2)

#ノイズ処理
img3=cv2.medianBlur(img2,55)
cv2.imwrite(name+"_denoised.jpg",img3)

#円検出
circles = cv2.HoughCircles(img3, cv2.HOUGH_GRADIENT, dp=1.0, minDist=2000, param1=100, param2=2147483650, minRadius=0, maxRadius=0)
try :
    circles = np.uint16(np.around(circles))
    for circle in circles[0,:]:
         print(circle[0])
         circle_x=circle[0]
         circle_y=circle[1]
         radius=circle[2]
 

    # 円周を描画する
    cv2.circle(img, (circle_x, circle_y), radius, (0,0,255), 5)
    # 中心点を描画する
    cv2.circle(img, (circle_x, circle_y), 2, (0, 0, 255), 3)
    #中心線を描画する
    cv2.line(img,(circle_x,1000),(circle_x,0),(0,255,0),3,cv2.LINE_AA,0)
    cv2.imwrite(name+"_after.jpg", img)
    
    #円の内部を切り取り
    img4=img3[int(circle_y-radius/1.4):int(circle_y+radius/1.4),int(circle_x-radius/1.4):int(circle_x+radius/1.4)]
    whole_pixel=img4.size
    blue_pixel=cv2.countNonZero(img4)
    cv2.imwrite(name+"_cut.jpg",img4)
    #ボールがあるか検出
    proportion=blue_pixel/whole_pixel*100
    if proportion>90:
        print("there is a ball")
    else :
        print("there is no ball")

except :
    print("circle was not found")
    sys.exit()


