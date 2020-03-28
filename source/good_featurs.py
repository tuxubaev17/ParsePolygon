import numpy as np
import cv2 as cv

img = cv.imread('screens/output.png')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

corners = cv.goodFeaturesToTrack(gray, 100, 0.09, 10)

corners = np.int0(corners)

for i in corners:
    x, y = i.ravel()
    cv.circle(img, (x, y), 3, [0, 150, 0], -1)

for i in range(1, len(corners)):
    print(corners[i])

cv.imshow('Shi-Tomasi Corner Detector', img)
cv.imwrite('screens/test1.png', img)

if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()
