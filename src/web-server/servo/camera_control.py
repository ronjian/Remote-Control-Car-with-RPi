import RPi.GPIO as GPIO  
import time   

class CONTROL:
	def __init__(self, STRIDE= 0.01, NOMINAL=7.5, RANGE=3.5):
		self.STRIDE= STRIDE 
		self.NOMINAL= NOMINAL 
		self.RANGE = RANGE  
		self.previous_hor_dc = self.NOMINAL
		self.previous_ver_dc = self.NOMINAL

		GPIO.setmode(GPIO.BCM)  
		GPIO.setup(19, GPIO.OUT, initial=False)  
		self.horizontal = GPIO.PWM(19,50)
		self.horizontal.start(self.NOMINAL)  
		time.sleep(1)  

		GPIO.setup(26, GPIO.OUT, initial=False)  
		self.vertical = GPIO.PWM(26,50)
		self.vertical.start(self.NOMINAL)  
		time.sleep(1)  

		self.MAX_DC = self.NOMINAL +  self.RANGE
		self.MIN_DC = self.NOMINAL -  self.RANGE

	def horizontal_move(self,direction=1.0):
	    dutycycle = self.previous_hor_dc + direction * self.RANGE * self.STRIDE
	    if dutycycle > self.MAX_DC: 
	    	dutycycle = self.MAX_DC
	    elif dutycycle < self.MIN_DC:
	    	dutycycle = self.MIN_DC
	    self.horizontal.ChangeDutyCycle(dutycycle)  
	    self.previous_hor_dc = dutycycle

	def vertical_move(self,direction=1.0):
	    dutycycle = self.previous_ver_dc + direction * self.RANGE * self.STRIDE
	    if dutycycle > self.MAX_DC: 
	    	dutycycle = self.MAX_DC
	    elif dutycycle < self.MIN_DC:
	    	dutycycle = self.MIN_DC
	    self.vertical.ChangeDutyCycle(dutycycle)  
	    self.previous_ver_dc = dutycycle

	def reset(self):
		self.vertical.ChangeDutyCycle(self.NOMINAL)
		self.horizontal.ChangeDutyCycle(self.NOMINAL)  
		self.previous_hor_dc = self.NOMINAL
		self.previous_ver_dc = self.NOMINAL

	def reset_for_capture(self, ver_angle=7.5, hor_angle=7.5):
		self.vertical.ChangeDutyCycle(ver_angle)
		self.horizontal.ChangeDutyCycle(hor_angle)  

	def close(self):
		GPIO.cleanup()