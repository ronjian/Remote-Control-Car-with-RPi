import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
	def __init__(self, TRIG = 16, ECHO = 12):
		GPIO.setmode(GPIO.BCM)
		self.TRIG = TRIG 
		self.ECHO = ECHO
		GPIO.setup(self.TRIG, GPIO.OUT)
		GPIO.setup(self.ECHO, GPIO.IN)
		GPIO.output(self.TRIG, False)
		time.sleep(1)
		print("Ultrasonic sensor (trigger pin: %s, echo pin: %s) is settled"\
		 % (self.TRIG, self.ECHO))

	def detect(self):
		#trigger
		GPIO.output(self.TRIG, True)
		time.sleep(0.00001)
		GPIO.output(self.TRIG, False)
		#echo
		while GPIO.input(self.ECHO)==0:
			pulse_start = time.time()
		while GPIO.input(self.ECHO)==1:
			pulse_end = time.time()
		#calculation
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance, 2)
		return distance
