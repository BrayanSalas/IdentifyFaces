import cv2
import time

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
i = 0

while True:
    rval, frame = vc.read()
    cv2.imshow("preview", frame)
    key = cv2.waitKey(20)
    cv2.imwrite("./Karla Franco/foto" + str(i) + '.jpg', frame)
    i = i + 1
    if key == 27: # exit on ESC
        print("Toma de foto terminada")
        break
cv2.destroyWindow("preview")
vc.release()