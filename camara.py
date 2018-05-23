import time
import picamera

with picamera.PiCamera() as picam:
	picam.start_preview()
	time.sleep(7)
	i = 0
	while (i<30):
		picam.capture('foto'+ str(i) +'.jpg')
		i = i + 1
	picam.stop_preview()
	picam.close()
time.sleep(5)
