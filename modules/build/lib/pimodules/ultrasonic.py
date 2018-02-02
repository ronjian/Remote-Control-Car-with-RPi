import RPi.GPIO as GPIO
from time import sleep, time

class CONTROL:
	def __init__(self, TRIG, ECHO):
		self.TRIG = TRIG 
		self.ECHO = ECHO
		self.start()

	def start(self):
		GPIO.setmode(GPIO.BCM)

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
					raise ValueError("Stuck in loop1, break, PIN is trigger:{} echo:{}".format(self.TRIG, self.ECHO))
			while GPIO.input(self.ECHO)==1:
				pulse_end = time()
				if pulse_end - start_time > 0.3: 
					raise ValueError("Stuck in loop2, break, PIN is trigger:{} echo:{}".format(self.TRIG, self.ECHO))
			#calculation
			pulse_duration = pulse_end - pulse_start
			distance = pulse_duration * 17150
			distance = round(distance, 2)
		except Exception as e:
			# print(str(e))
			print("detection error")
			distance = 0.0
		finally:
			return distance

	def close(self):
		GPIO.cleanup()
