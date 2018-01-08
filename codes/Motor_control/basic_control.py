#!/usr/bin/env python3
import threading
import time
import curses
import RPi.GPIO as GPIO
import argparse


def monitor_key():
	"""
	Because package "curses" can't detect key release action.
	So make this function to monitor the key action by inquirying 
	the key action infinitely with a delay time, think key is released.
	This function will be kick off in another thread from the main process, 
	working as a daemon thread.
	"""
	global char, thl  # share key and thread lock with main process
	#initialize curses components
	screen = curses.initscr()
	curses.noecho() 
	curses.cbreak()
	screen.keypad(True)
	# define the delay time in millionseconds.
	# If timeout, screen.getch() will return -1. 
	# -1 will be treated as STOP command.
	# So the RC car will have ~0.3s latency.
	screen.timeout(FLAGS.delay)  
	try:
			while True:  
				tmp = screen.getch()
				thl.acquire()
				char = tmp
				thl.release()
	finally:
		# Close curses components properly, inc turn echo back on!
		curses.nocbreak()
		screen.keypad(0)
		curses.echo()
		curses.endwin()


def init():
	"""
	Initialize GPIO pin in BCM("Broadcom SOC channel") mode
	"""
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17, GPIO.OUT)
	GPIO.setup(22, GPIO.OUT)
	GPIO.setup(23, GPIO.OUT)
	GPIO.setup(24, GPIO.OUT)
	
def stop():
	"""stop car"""
	GPIO.output(17, False)
	GPIO.output(22, False)
	GPIO.output(23, False) 
	GPIO.output(24, False)

def right(forward=True):
	"""
	Control right side wheels

	Args:
	- forward: control the right side wheels cycle to move the car forward,
		if "False", right side wheels will cycle to move the car backward.
	"""
	GPIO.output(17, forward)
	GPIO.output(22, not forward)

def left(forward=True):
	"""
	Control left side wheels

	Args:
	- forward: control the left side wheels cycle to move the car forward,
		if "False", left side wheels will cycle to move the car backward.
	"""
	GPIO.output(23, forward) 
	GPIO.output(24, not forward)


def forward(forward=True):
	"""
	Control both side wheels to cycle in the same direction.

	Args:
	- forward: default as "True" to control both side wheels to cycle 
		to move the car forward.
		if False: both side wheels will cycle to move the car backward.
	"""
	left(forward=forward)
	right(forward=forward)

def left_cycle(forward=True):
	"""
	Control two sides wheels to cycle in opposite direction
	 to make the car cycling.

	Args:
	- forward: If "True", the car will cycle in left. 
		If "False", the car will cycle in right.
	"""
	left(forward=forward)
	right(forward=not forward)


#main
if __name__ == '__main__':
	#read arguments
	parser = argparse.ArgumentParser(description="Remote control PRI car.")
	parser.add_argument(
		'--delay', 
		type=int,
		default=250,
		help="Give the expecting delay time for the RC car, it's in millionseconds and at least 200 millionseconds."
		)
	FLAGS, unparsed = parser.parse_known_args()

	init()  #init GPIO
	char = -1
	prev_cmd = -1
	thl = threading.Lock()	
	#start a thread to monitor keyboard action	
	threading.Thread(target = monitor_key, args = ()).start()  
	#detect keyboard input to control RC car
	try:
		while True:  
			thl.acquire()
			cmd = char
			thl.release()
			if cmd != prev_cmd:
				if cmd == ord('q'):
					print("QUIT")
					break
				elif cmd == curses.KEY_UP:
					print("FORWARD")
					forward(forward=True)
				elif cmd == curses.KEY_DOWN:
					print("BACKWARD")
					forward(forward=False)
				elif cmd == curses.KEY_RIGHT:
					print("CYCLY RIGHT")
					left_cycle(forward=False)
				elif cmd == curses.KEY_LEFT:
					print("CYCLE LEFT")
					left_cycle(forward=True)
				elif cmd == -1:
					print("STOP")
					stop()   

				prev_cmd = cmd

			time.sleep(FLAGS.delay / 1000.0 * 1.5 )

	finally:
		# clean GPIO
		stop()
		GPIO.cleanup()



