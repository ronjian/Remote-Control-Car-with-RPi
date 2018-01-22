import time 
import picamera
from servo import camera_control
import os

if __name__ == "__main__":
	# tuning camera servo
	cc = camera_control.CONTROL()
	cc.reset_for_capture(ver_angle=7.2, hor_angle=7.7)
	time.sleep(3)
	cc.close()

	# initial camera
	camera = picamera.PiCamera()
	camera.resolution = (400, 300)
	camera.rotation = 180
	# camera warm-up time
	time.sleep(2)

	# capturing
	duration_min = 15
	start_time = time.time()
	end_time = start_time + duration_min * 60
	folder = "./assets/" + time.strftime("%Y%m%d_%H%M%S" + "/")
	os.mkdir(folder)
	while time.time() < end_time:
		camera.capture(folder + str(time.time()) +".jpg")
		time.sleep(1)