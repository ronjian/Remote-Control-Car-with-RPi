import ultrasonic_pigpio_left as left
import ultrasonic_pigpio_right as right
import ultrasonic_pigpio_front as front
while 1:
 print(left.readDistance())
 print(right.readDistance())
 print(front.readDistance())