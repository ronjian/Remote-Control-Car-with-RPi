import RPi.GPIO as GPIO
import time

if __name__ == '__main__':
	TrackingPin = 6
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(TrackingPin, GPIO.OUT)
	try:
		while True:
			GPIO.output(TrackingPin, GPIO.LOW)
			time.sleep(0.3)
			GPIO.output(TrackingPin, GPIO.HIGH)
			time.sleep(1)
	except KeyboardInterrupt:
	 GPIO.cleanup()