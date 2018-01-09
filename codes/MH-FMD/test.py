import RPi.GPIO as GPIO
import time

if __name__ == '__main__':
	TrackingPin = 6
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(TrackingPin, GPIO.OUT)
	try:
		while True:
			GPIO.output(TrackingPin, GPIO.HIGH)
			time.sleep(1)
			# GPIO.cleanup(TrackingPin)
			time.sleep(5)
	except KeyboardInterrupt:
	 GPIO.cleanup()