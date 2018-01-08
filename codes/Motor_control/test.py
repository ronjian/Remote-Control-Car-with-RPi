# import curses and GPIO
import curses
import RPi.GPIO as GPIO

#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)

try:
        while True:   
            char = screen.getch()
            if char == ord('q'):
                break
            elif char == curses.KEY_UP:
                print("up")
                GPIO.output(17,False)
                GPIO.output(22,True)
                GPIO.output(23,False)
                GPIO.output(24,True)
            elif char == curses.KEY_DOWN:
                print("down")
                GPIO.output(17,True)
                GPIO.output(22,False)
                GPIO.output(23,True)
                GPIO.output(24,False)
            elif char == curses.KEY_RIGHT:
                print("right")
                GPIO.output(17,True)
                GPIO.output(22,False)
                GPIO.output(23,False)
                GPIO.output(24,True)
            elif char == curses.KEY_LEFT:
                print("left")
                GPIO.output(17,False)
                GPIO.output(22,True)
                GPIO.output(23,True)
                GPIO.output(24,False)
            elif char == 10:
                GPIO.output(17,False)
                GPIO.output(22,False)
                GPIO.output(23,False)
                GPIO.output(24,False)
             
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    GPIO.cleanup()
    
