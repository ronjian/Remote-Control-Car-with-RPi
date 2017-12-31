import curses
import RPi.GPIO as gpio
import time
 
def init():
 gpio.setmode(gpio.BCM)
 gpio.setup(17, gpio.OUT)
 gpio.setup(22, gpio.OUT)
 gpio.setup(23, gpio.OUT)
 gpio.setup(24, gpio.OUT)
 
def forward():
 gpio.output(17, True)
 gpio.output(22, False)
 gpio.output(23, True) 
 gpio.output(24, False)
 
def reverse():
 gpio.output(17, False)
 gpio.output(22, True)
 gpio.output(23, False) 
 gpio.output(24, True)

def left():
 gpio.output(17, False)
 gpio.output(22, True)
 gpio.output(23, True) 
 gpio.output(24, False)

def right():

 gpio.output(17, True)
 gpio.output(22, False)
 gpio.output(23, False) 
 gpio.output(24, True)

def stop():
 gpio.output(17, False)
 gpio.output(22, False)
 gpio.output(23, False) 
 gpio.output(24, False)
 
init()
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
                forward()
            elif char == curses.KEY_DOWN:
                print("reverse")
                reverse()
            elif char == curses.KEY_RIGHT:
                print("right")
                right()
            elif char == curses.KEY_LEFT:
                print("left")
                left()
            #space key
            elif char == 32:
                print("stop")
                stop()   
             
finally:
    stop()
    gpio.cleanup()
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
