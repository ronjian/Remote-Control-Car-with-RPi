"""An example to blink an LED once every 0.2 seconds:"""
import RPi.GPIO as GPIO

PIN = 06

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

p = GPIO.PWM(PIN, 5) # frequency
p.start(1)
input('Press return to stop:')   # use raw_input for Python 2
p.stop()
GPIO.cleanup()
