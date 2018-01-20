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
		time.sleep(0.5)
		print("Ultrasonic sensor (trigger pin: %s, echo pin: %s) is settled"\
		 % (self.TRIG, self.ECHO))

	def detect(self):
		start_time = time.time()
		#trigger
		GPIO.output(self.TRIG, True)
		time.sleep(0.00001)
		GPIO.output(self.TRIG, False)
		try:
			#echo
			while GPIO.input(self.ECHO)==0:
				pulse_start = time.time()
				pulse_end = pulse_start
				if pulse_start - start_time > 0.3: 
					print("Stuck in while1, break")
					break
			while GPIO.input(self.ECHO)==1:
				pulse_end = time.time()
				if pulse_end - start_time > 0.3: 
					print("Stuck in while1, break")
					break
			#calculation
			pulse_duration = pulse_end - pulse_start
			distance = pulse_duration * 17150
			distance = round(distance, 2)
		except e:
			print(e)
			distance = 0.0
		return distance
