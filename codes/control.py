#!/usr/bin/env python3
import threading
import time
import curses
import RPi.GPIO as gpio

def monitor_key():
	global char, thl
	screen = curses.initscr()
	curses.noecho() 
	curses.cbreak()
	screen.keypad(True)
	screen.timeout(300)#0.3 second waiting, if timeout, screen.getch() will return -1. 
	try:
			while True:  
				tmp = screen.getch()
				thl.acquire()
				char = tmp
				thl.release()
	finally:
		#Close down curses properly, inc turn echo back on!
		curses.nocbreak()
		screen.keypad(0)
		curses.echo()
		curses.endwin()

def init():
    """initial GPIO pin in BCM("Broadcom SOC channel") mode"""
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)
    
def stop():
    """stop car"""
    gpio.output(17, False)
    gpio.output(22, False)
    gpio.output(23, False) 
    gpio.output(24, False)

def right(forward=True):
    """control right side wheels"""
    gpio.output(17, forward)
    gpio.output(22, not forward)

def left(forward=True):
    """control left side wheels"""
    gpio.output(23, forward) 
    gpio.output(24, not forward)


def forward(forward=True):
    """
    - forward=True: both side wheels forward
    - forward=False: both side wheels backward
    """
    left(forward=forward)
    right(forward=forward)

def left_cycle(forward=True):
    """
    - forward=True: turning left
    - forward=False: turning right
    """
    left(forward=forward)
    right(forward=not forward)



if __name__ == '__main__':
    #init GPIO
	init()
    #start a thread to monitor keyboard action
    char = -1
	prev_cmd = -1
	thl = threading.Lock()
	threading.Thread(target = monitor_key, args = ()).start()
    #detect keyboard input to control RC car
	try:
		while True:  
            thl.acquire()
			cmd = char
            thl.release()
			if cmd != prev_cmd:
				if cmd == ord('q'):
					break
				elif cmd == curses.KEY_UP:
					print("forward")
					forward(forward=True)
				elif cmd == curses.KEY_DOWN:
					print("reverse")
					forward(forward=False)
				elif cmd == curses.KEY_RIGHT:
					print("right_cycle")
					left_cycle(forward=False)
				elif cmd == curses.KEY_LEFT:
					print("left_cycle")
					left_cycle(forward=True)
				elif cmd == -1:
					print("stop")
					stop()   

                prev_cmd = cmd

			time.sleep(0.4)

	finally:
		# clean GPIO
		stop()
		gpio.cleanup()



