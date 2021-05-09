import numpy as np
import cv2 as cv

img = "resources/down.PNG"  # картинка
img = cv.imread(img)


def find_lines(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  #перевод картинки в оттенки серого для передачи в canny
    canny = cv.Canny(gray, 50, 50)  # рисуем все контуры которые нашли
    lines = cv.HoughLinesP(canny, rho=1, theta=1*np.pi/180, threshold=50, minLineLength=50, maxLineGap=50)  # все найденные контуры разделяем на линии
    N = lines.shape[0]
    for i in range(N):
        x1 = lines[i][0][0]
        y1 = lines[i][0][1]
        x2 = lines[i][0][2]
        y2 = lines[i][0][3]
        if x1 == x2:  # отсекаем все горизонтальные и вертикальные линии
            pass
        elif y1 == y2:
            pass
        else:
            cv.line(img,(x1,y1),(x2,y2),(0,0,0),2)  #рисуем линии острия стрелки


def search_corner(img):

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    (_ret, threshold) = cv.threshold(hsv[:,:,1], 90, 255, cv.THRESH_OTSU)
    dist = cv.distanceTransform(threshold, cv.DIST_L2, cv.DIST_MASK_PRECISE)  # заменяем значение каждого пикселя его ростоянием до ближайщего пикселя фона
    idx = np.argmax(dist)
    y,x = np.unravel_index(idx, dist.shape)
    M = cv.moments(threshold)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    a = (180*np.arctan2(x-cX, y-cY)/np.pi)  #поиск угла соединения двух линий

    if 179 < a < 181:
        print("вверх")
    elif -1 < a < 1:
        print("вниз")
    elif -89 > a > -91:
        print("влево")
    elif 89 < a < 91:
        print("вправо")
    else:
        pass

find_lines(img)
search_corner(img)


cv.imshow('orig', img)
cv.waitKey()
cv.destroyAllWindows()

