from types import NoneType
import cv2
import numpy as np
import sys

img = cv2.imread("./350806.png")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=0.8, minDist=200, param1=100, param2=95, minRadius=0, maxRadius=0)

try :
    a=np.around(circles)
except :
    print("circle was not found")
    sys.exit()


circles = np.uint16(np.around(circles))

for circle in circles[0, :]:
    # 円周を描画する
    cv2.circle(img, (circle[0], circle[1]), circle[2], (0, 165, 255), 5)
    # 中心点を描画する
    cv2.circle(img, (circle[0], circle[1]), 2, (0, 0, 255), 3)


cv2.imwrite("350806_after.png", img)
