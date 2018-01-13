#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
p = GPIO.PWM(23, 50) 
p.start(0)
GPIO.output(24, False)
try:
    while 1:
    	# low to high
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.2)
        # high to low
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.2)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()