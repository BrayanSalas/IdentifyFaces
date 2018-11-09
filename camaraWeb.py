import cv2

class CamaraWeb:
    def tomarFoto():
        cv2.namedWindow("preview")
        vc = cv2.VideoCapture(0)

        while True:
            rval, frame = vc.read()
            cv2.imshow("preview", frame)
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                cv2.imwrite("foto.jpg", frame)
                print("Foto tomada correctamente")
                break
        cv2.destroyWindow("preview")
        vc.release()

        