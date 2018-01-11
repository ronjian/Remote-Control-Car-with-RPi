import RPi.GPIO as GPIO
import time

if __name__ == '__main__':
 TrackingPin = 21
 GPIO.setmode(GPIO.BCM)
 GPIO.setup(TrackingPin, GPIO.IN)

 try:
  while True:
   flag = GPIO.input(TrackingPin)
   if not flag:
    print time.strftime("%H:%M:%S") + 'something closing!'
   time.sleep(0.1)
 except KeyboardInterrupt:
  print "Bye"

 GPIO.cleanup()