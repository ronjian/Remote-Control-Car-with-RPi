import RPi.GPIO as GPIO
import time

class Alert:
	def __init__(self, PIN=6):
		self.TrackingPin = PIN
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.TrackingPin, GPIO.OUT, initial=GPIO.HIGH)

	def alert(self):
		while True:
			GPIO.output(self.TrackingPin, GPIO.LOW)
			time.sleep(0.1)
			GPIO.output(self.TrackingPin, GPIO.HIGH)
			time.sleep(2)

	def clean():
		GPIO.output(self.TrackingPin, GPIO.HIGH)
