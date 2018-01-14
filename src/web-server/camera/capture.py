import time 
import picamera

class Camera:
	def __init__(self):
		self.camera = picamera.PiCamera()
		self.camera.resolution = (1024, 768)
		self.camera.rotation = 180
		# Camera warm-up time
		time.sleep(2)

	def take_photo(self):
		self.camera.capture("assets/"+ time.strftime("%Y%m%d%H%M%S") +".jpg")