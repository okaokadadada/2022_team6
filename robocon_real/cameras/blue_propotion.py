import sys
import cv2
import numpy as np

# 読み込みファイルの名前
filename_read = "./robocon_ball4.jpg"
# 書き込みファイルの名前
filename_write = "./robocon_ball4_4_detected.jpg"



# ファイルの読み込み
img = cv2.imread(filename_read)
# 画像のサイズを下げる.(1/4)
img = cv2.resize(img, dsize=(int(img.shape[1]/4), int(img.shape[0]/4)))

# 画像サイズを取得
hight = img.shape[0]
width = img.shape[1]

# 画像をグレースケールに変更
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 円検出
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=0.7, minDist=500, param1=100, param2=10, minRadius=10)


try :
    a=np.around(circles)
except :
    print("circle was not found")
    sys.exit()


circles = np.uint16(np.around(circles))

print(circles)

# Bの平均値の最大値
b_ave_best = 0
# Bの平均値の最大値を持つ円のパラメータ
circle_best  = circles[0, 0, :]

# 円内部のBの値の平均をとり、比較する
for circle in circles[0, :]:
    
    x_center = circle[0]
    y_center = circle[1]
    radius = circle[2]

    b_value = 0
    b_value_inn = 0
    i = 0

    for y in range(hight):
        for x in range(width):
            b_value += img[y,x,0]

            if (x - x_center)**2+(y - y_center)**2 < radius**2:
                b_value_inn += img[y,x,0]
                i += 1

    b_ave = b_value / (hight*width)
    b_ave_inn = b_value_inn / i

    if b_ave_best < b_ave_inn:

        blue_average_best = b_ave_inn
        circle_best = circle 


# 円周を描画する
cv2.circle(img, (circle_best[0], circle_best[1]), circle_best[2], (0, 165, 255), 5)
# 中心点を描画する
cv2.circle(img, (circle_best[0], circle_best[1]), 2, (0, 0, 255), 3)


cv2.imwrite(filename_write, img)
