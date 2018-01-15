import RPi.GPIO as GPIO
import time 

PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

while True:
	print(GPIO.input(PIN))
	time.sleep(0.01)