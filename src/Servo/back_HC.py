import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pin_number = 18
GPIO.setup(pin_number, GPIO.OUT)

# Now we can use PWM on pin 11.  It's software PWM, so don't expect perfect
# results.  Linux is a multitasking OS so other processes could interrupt
# the process which generate the PWM signal at any time.
# Raspberry Pi has a hardware PWm channel, but this Pythong library
# does not yet support it.  
frequency_hertz = 50
pwm = GPIO.PWM(pin_number, frequency_hertz)


# How to position a servo?  All servos are pretty much the same.
# Send repeated purses of an absolute duration (not a relative duty cycle)
# between 0.40 ms and 2.5 ms in duration.  A single pulse will only move it
# a short distance in the desired direction.  Repeated pulses will continue
# its movement and then once it arrives at the specified position it will
# insruct the motor to forcefully hold its position.
left_position = 2.2
right_position = 1.3 
middle_position = (right_position + left_position) / 2 

# I'll store a sequence of positions for use in a loop later on.
positionList = [left_position, middle_position, right_position, middle_position]

# total number of milliseconds in a a cycle.  Given this, we will then 
# know both how long we want to pulse in this cycle and how long the 
# cycle itself is.  That is all we need to calculate a duty cycle as 
# a percentage.
ms_per_cycle = 1000 / frequency_hertz

# Iterate through the positions sequence 3 times.
for i in range(5):
	# This sequence contains positions from left to right
	# and then back again.  Move the motor to each position in order.
	for position in positionList:
		duty_cycle_percentage = position * 100 / ms_per_cycle
		print("Position: " + str(position))
		print("Duty Cycle: " + str(duty_cycle_percentage))
		print("")
		pwm.start(duty_cycle_percentage)
		time.sleep(1)
	

# Done.  Terminate all signals and relax the motor.
pwm.stop()

# We have shut all our stuff down but we should do a complete
# close on all GPIO stuff.  There's only one copy of real hardware.
# We need to be polite and put it back the way we found it.
GPIO.cleanup()
