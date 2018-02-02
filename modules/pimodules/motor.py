import RPi.GPIO as GPIO

class CONTROL:

	def __init__(self, RIGHT_FRONT_PIN,\
						LEFT_FRONT_PIN,\
						RIGHT_BACK_PIN,\
						LEFT_BACK_PIN,\
						FREQUENCY=100):
		self.RIGHT_FRONT_PIN = RIGHT_FRONT_PIN
		self.LEFT_FRONT_PIN = LEFT_FRONT_PIN
		self.RIGHT_BACK_PIN = RIGHT_BACK_PIN
		self.LEFT_BACK_PIN = LEFT_BACK_PIN
		self.FREQUENCY = FREQUENCY
		self.start()

	def start(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.RIGHT_FRONT_PIN, GPIO.OUT)
		GPIO.setup(self.RIGHT_BACK_PIN, GPIO.OUT)
		GPIO.setup(self.LEFT_FRONT_PIN, GPIO.OUT)
		GPIO.setup(self.LEFT_BACK_PIN, GPIO.OUT)
		self.right_forward = GPIO.PWM(self.RIGHT_FRONT_PIN, self.FREQUENCY) 
		self.right_forward.start(0)
		self.right_backward = GPIO.PWM(self.RIGHT_BACK_PIN, self.FREQUENCY) 
		self.right_backward.start(0)
		self.left_forward = GPIO.PWM(self.LEFT_FRONT_PIN, self.FREQUENCY) 
		self.left_forward.start(0)
		self.left_backward = GPIO.PWM(self.LEFT_BACK_PIN, self.FREQUENCY) 
		self.left_backward.start(0)

	def stop(self):
		"""stop car"""
		self.left_forward.ChangeDutyCycle(0)
		self.left_backward.ChangeDutyCycle(0)
		self.right_forward.ChangeDutyCycle(0)
		self.right_backward.ChangeDutyCycle(0)

	def __inner_right(self, dc_pct=100.0):
		"""
		Control left side wheels

		Args:

		"""
		if dc_pct > 0 :
			self.right_forward.ChangeDutyCycle(dc_pct)
		else:
			self.right_backward.ChangeDutyCycle(-1 * dc_pct)

	def __inner_left(self, dc_pct=100.0):
		"""
		Control right side wheels

		Args:

		"""
		if dc_pct > 0 :
			self.left_forward.ChangeDutyCycle(dc_pct)
		else:
			self.left_backward.ChangeDutyCycle(-1 * dc_pct)


	def forward(self, dc_pct=100.0):
		"""
		Control both side wheels to cycle forward.

		Args:

		"""
		self.stop()
		self.__inner_right(dc_pct)
		self.__inner_left(dc_pct)

	def backward(self, dc_pct=100.0):
		"""
		Control both side wheels to cycle in the same direction.

		Args:

		"""
		self.stop()
		self.forward(-1 * dc_pct)


	def left(self, dc_pct=100.0):
		"""
		Control two sides wheels to cycle in opposite direction
		 to make the car cycling.

		Args:

		"""
		self.stop()
		self.__inner_left(dc_pct)
		self.__inner_right(-1 * dc_pct)

	def right(self, dc_pct=100.0):
		"""
		Control two sides wheels to cycle in opposite direction
		 to make the car cycling.

		Args:

		"""
		self.stop()
		self.left(-1 * dc_pct)

	def close(self):
		GPIO.cleanup()

