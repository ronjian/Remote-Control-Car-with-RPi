import RPi.GPIO as GPIO  
from time import sleep

class CONTROL:
	"""
	This module abstract the action of a typical servo by software PWM: 
	1. little step cycle in two opposite direction choices
	2. direct cycle to specific angle
	3. reset to initial angle

	Be careful to set the range to protest your servo.
	"""
	def __init__(self, PIN, STRIDE= 0.01, NOMINAL=7.5, RANGE=3.9):
		self.STRIDE= STRIDE # step magnitude
		self.NOMINAL= NOMINAL  # initial digital cycle/angle
		self.RANGE = RANGE  # range limitation
		self.previous_dc = self.NOMINAL # tracking the previous angle
		self.MAX_DC = self.NOMINAL +  self.RANGE # high limit
		self.MIN_DC = self.NOMINAL -  self.RANGE # low limit
		self.PIN = PIN
		self.start()

	def start(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.PIN, GPIO.OUT, initial=False)  
		self.PWM = GPIO.PWM(self.PIN,50)
		self.PWM.start(self.NOMINAL)
		# give time to cycle
		sleep(1)

	def step_move(self,direction=1.0):
		"""
		Cycle servo a little step.
		This function can only control the direction.

		Limit: servo can't cycle out of the given range.

		:param direction: 1.0 or -1.0
		"""
		dc = self.previous_dc + direction * self.RANGE * self.STRIDE
		if dc > self.MAX_DC or dc < self.MIN_DC:
			print("WARNING!! The servo reached the limit.")
		else:
			self.PWM.ChangeDutyCycle(dc)  
			self.previous_dc = dc


	def direct_move(self, dc, given_time = 1.0):
		"""
		Cycle the servo directly to specific angle.
		The servo works in async with this function.
		Make sure giving the servo some time to move
		before giving it other commands.
		
		Limit: servo can't cycle out of the given range.

		:param dc: digital cycle, can be treat as postion 
		of ther servo
		:param given_time: give servo time to cycle 
		to position

		"""
		if dc > self.MAX_DC:
			print("WARNING!! {} is higher than the high limit {}".format(dc, self.MAX_DC))
			dc = self.MAX_DC
		elif dc < self.MIN_DC:
			print("WARNING!! {} is lower than the low limit {}".format(dc, self.MIN_DC))
			dc = self.MIN_DC
			
		self.PWM.ChangeDutyCycle(dc)
		if given_time > 0.0: sleep(given_time)
		self.previous_dc = dc


	def reset(self):
		"""
		reset to initial angle
		"""
		self.direct_move(self.NOMINAL)

	def stop(self, reset=True):
		"""
		make sure to invoke this function 
		to quit your program elegantly
		"""
		if reset:
			self.reset()
		self.PWM.stop()

	def close(self, reset=True):
		self.stop(reset=reset)
		GPIO.cleanup()

