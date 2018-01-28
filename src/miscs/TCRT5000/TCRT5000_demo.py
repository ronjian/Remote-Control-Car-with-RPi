import RPi.GPIO as GPIO
import time

TrackingPin = 25

def setup():
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(TrackingPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def loop():

 previous_flag = None
 while True:
  flag = GPIO.input(TrackingPin)
  if flag == GPIO.LOW and flag != previous_flag:
   print time.strftime("%H:%M:%S") + ' On the path...'
  elif flag != GPIO.LOW:
   print time.strftime("%H:%M:%S") + ' Out of path, turn back!!!'
  previous_flag = flag
  #give delay
  time.sleep(0.1)

def destroy():
 GPIO.cleanup()

if __name__ == '__main__':
 setup()
try:
 loop()
except KeyboardInterrupt:
 destroy()