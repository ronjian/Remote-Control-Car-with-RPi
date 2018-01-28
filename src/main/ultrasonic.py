import RPi.GPIO as GPIO
from time import sleep, time

class CONTROL:
	def __init__(self, TRIG, ECHO):
		self.start(TRIG, ECHO)

	def start(self, TRIG, ECHO):
		GPIO.setmode(GPIO.BCM)
		self.TRIG = TRIG 
		self.ECHO = ECHO
		GPIO.setup(self.TRIG, GPIO.OUT)
		GPIO.setup(self.ECHO, GPIO.IN)
		GPIO.output(self.TRIG, False)
		sleep(0.5)

	def detect(self):
		start_time = time()
		#trigger
		GPIO.output(self.TRIG, True)
		sleep(0.00001)
		GPIO.output(self.TRIG, False)
		try:
			#echo
			while GPIO.input(self.ECHO)==0:
				pulse_start = time()
				pulse_end = pulse_start
				if pulse_start - start_time > 0.3: 
					print("Stuck in while1, break, PIN is trigger:{} echo:{}".format(self.TRIG, self.ECHO))
					break
			while GPIO.input(self.ECHO)==1:
				pulse_end = time()
				if pulse_end - start_time > 0.3: 
					print("Stuck in while2, break")
					break
			#calculation
			pulse_duration = pulse_end - pulse_start
			distance = pulse_duration * 17150
			distance = round(distance, 2)
		except Exception:
			distance = 0.0
		finally:
			return distance

	def close(self):
		GPIO.cleanup()
