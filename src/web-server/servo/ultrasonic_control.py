import RPi.GPIO as GPIO  
import time   

class CONTROL:
	def __init__(self, STRIDE= 0.01, NOMINAL=7.5, RANGE=3.5, PIN=18):
		self.STRIDE= STRIDE 
		self.NOMINAL= NOMINAL 
		self.RANGE = RANGE  
		self.previous_hor_dc = self.NOMINAL

		GPIO.setmode(GPIO.BCM)  
		GPIO.setup(PIN, GPIO.OUT, initial=False)  
		self.horizontal = GPIO.PWM(PIN,50)
		self.horizontal.start(self.NOMINAL)  
		time.sleep(1)  

		self.MAX_DC = self.NOMINAL +  self.RANGE
		self.MIN_DC = self.NOMINAL -  self.RANGE
		print("init %s success" % PIN)

	def horizontal_move(self,direction=1.0):
	    dutycycle = self.previous_hor_dc + direction * self.RANGE * self.STRIDE
	    print(dutycycle)
	    if dutycycle > self.MAX_DC: 
	    	dutycycle = self.MAX_DC
	    elif dutycycle < self.MIN_DC:
	    	dutycycle = self.MIN_DC
	    self.horizontal.ChangeDutyCycle(dutycycle)  
	    self.previous_hor_dc = dutycycle

	def reset(self):
		self.horizontal.ChangeDutyCycle(self.NOMINAL)  
		self.previous_hor_dc = self.NOMINAL
