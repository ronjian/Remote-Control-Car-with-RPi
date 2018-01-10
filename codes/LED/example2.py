"""An example to brighten/dim an LED"""
import time
import RPi.GPIO as GPIO

PIN = 06

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

p = GPIO.PWM(PIN, 50)  # channel=12 frequency=50Hz
p.start(0)
try:
    while 1:
    	# dim to bright
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        # bright to dim
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()