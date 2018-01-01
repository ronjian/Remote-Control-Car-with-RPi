#!/usr/bin/env python3
import curses
import RPi.GPIO as gpio
import time

def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)
    
def stop():
    gpio.output(17, False)
    gpio.output(22, False)
    gpio.output(23, False) 
    gpio.output(24, False)
    
def right(forward=True):
    gpio.output(17, forward)
    gpio.output(22, not forward)

def left(forward=True):
    gpio.output(23, forward) 
    gpio.output(24, not forward)


def forward(forward=True):
    stop()
    left(forward=forward)
    right(forward=forward)

def left_cycle(forward=True):
    stop()
    left(forward=forward)
    right(forward=not forward)

def right_cycle(forward=True):
    stop()
    left(forward=not forward)
    right(forward=forward)


if __name__ == "__main__":
    #init GPIO
    init()
    stop()
    # Get the curses window, turn off echoing of keyboard to screen, turn on
    # instant (no waiting) key response, and use special values for cursor keys
    screen = curses.initscr()
    curses.noecho() 
    curses.cbreak()
    screen.keypad(True)


    try:
            while True:   
                char = screen.getch()
                print(char)
                if char == ord('q'):
                    break
                elif char == curses.KEY_UP:
                    print("forward")
                    forward(forward=True)
                elif char == curses.KEY_DOWN:
                    print("reverse")
                    forward(forward=False)
                elif char == curses.KEY_RIGHT:
                    print("right_cycle")
                    right_cycle(forward=True)
                elif char == curses.KEY_LEFT:
                    print("left_cycle")
                    left_cycle(forward=True)
                #space key
                elif char == 32:
                    print("stop")
                    stop()   

    finally:
        #clean GPIO
        stop()
        gpio.cleanup()
        #Close down curses properly, inc turn echo back on!
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()
