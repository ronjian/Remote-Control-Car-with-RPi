#!/usr/bin/env python3
import RPi.GPIO as GPIO

class CONTROL:

	def __init__(self, Frequency=2000):
		"""
		Initialize GPIO pin in BCM("Broadcom SOC channel") mode
		"""
		# GPIO.setwarnings(False)
		self.Frequency = Frequency

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(17, GPIO.OUT)
		GPIO.setup(22, GPIO.OUT)
		GPIO.setup(23, GPIO.OUT)
		GPIO.setup(24, GPIO.OUT)
		
		self.right_forward = GPIO.PWM(17, self.Frequency) 
		self.right_forward.start(0)
		self.right_backward = GPIO.PWM(22, self.Frequency) 
		self.right_backward.start(0)
		self.left_forward = GPIO.PWM(23, self.Frequency) 
		self.left_forward.start(0)
		self.left_backward = GPIO.PWM(24, self.Frequency) 
		self.left_backward.start(0)

	def stop(self):
		"""stop car"""
		self.left_forward.ChangeDutyCycle(0)
		self.left_backward.ChangeDutyCycle(0)
		self.right_forward.ChangeDutyCycle(0)
		self.right_backward.ChangeDutyCycle(0)

	def __inner_right(self, dc_pct=100):
		"""
		Control left side wheels

		Args:

		"""
		if dc_pct > 0 :
			self.right_forward.ChangeDutyCycle(dc_pct)
		else:
			self.right_backward.ChangeDutyCycle(-1 * dc_pct)

	def __inner_left(self, dc_pct=100):
		"""
		Control right side wheels

		Args:

		"""
		if dc_pct > 0 :
			self.left_forward.ChangeDutyCycle(dc_pct)
		else:
			self.left_backward.ChangeDutyCycle(-1 * dc_pct)


	def forward(self, dc_pct=100):
		"""
		Control both side wheels to cycle forward.

		Args:

		"""
		self.__inner_right(dc_pct)
		self.__inner_left(dc_pct)

	def backward(self, dc_pct=100):
		"""
		Control both side wheels to cycle in the same direction.

		Args:

		"""
		self.forward(-1 * dc_pct)


	def left(self, dc_pct=100):
		"""
		Control two sides wheels to cycle in opposite direction
		 to make the car cycling.

		Args:

		"""
		self.__inner_left(dc_pct)
		self.__inner_right(-1 * dc_pct)

	def right(self, dc_pct=100):
		"""
		Control two sides wheels to cycle in opposite direction
		 to make the car cycling.

		Args:

		"""
		self.left(-1 * dc_pct)

