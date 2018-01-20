<h2 id='gpio'>RPI3 GPIO Pin Mappings</h2>

https://pinout.xyz/

<p align="center">
<img src="assets/GPIO.png" width=600/><br>
<img src="assets/GPIO2.png" width=600/><br>
</p>


<h2 id='l298n'>Control motors by L298N</h2>

* Basic usage of L298N to control motors forward and backward:
    * http://www.piddlerintheroot.com/l298n-dual-h-bridge/
    * http://www.explainingcomputers.com/rasp_pi_robotics.html    
* Programming to use keyborad to control the motors:
    * Python curses package: https://docs.python.org/2/library/curses.html#constants  
    
There is two ways to control the motor speed. One is PWM changing on the INPUT pin as the below code snippet.
The other is using the enable PIN to change PWM, as [this code](https://github.com/custom-build-robots/Motor-Driver-L298N-H-Bridge/blob/master/L298NHBridge.py)
implemented. There is a [post](https://www.raspberrypi.org/forums/viewtopic.php?f=37&t=90243) comparing these two solutions.  
```python
#!/usr/bin/env python3
"""infinitely loop the motor to speed up and down"""
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
p = GPIO.PWM(23, 50) 
p.start(0)
GPIO.output(24, False)
try:
    while 1:
    	# low to high
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.2)
        # high to low
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.2)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()
```
* I use sublime to sync codes on my laptop with PI
    * https://www.youtube.com/watch?v=g6NqBGHFfm0
* [Steps](StreamRPIcamera.md) to stream PI camera video to laptop browser.
* [code sample](codes/basic_control.py) to control basic RC car (without speed control) by keyboard.
* check [here](http://www.toptechboy.com/raspberry-pi/raspberry-pi-lesson-27-analog-voltages-using-gpio-pwm-in-python/)
for PWM programming on RPi. [GPIO document](https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/) here.
[pigpio package](http://abyz.me.uk/rpi/pigpio/python.html) also implements controling PWM.

<h2 id='DHT11'>DHT11</h2>

Example code and tutorial:  
http://osoyoo.com/2017/03/21/%E6%A0%91%E8%8E%93%E6%B4%BE%E8%AF%BB%E5%8F%96dht11/  
<p align="center">
Diagram<br>
<img src="assets/dht11.png" width=300/><br>
Demo<br>
<img src="assets/DHT11_demo.png" width=400/><br>
</p>

<h2 id='TCRT5000'>TCRT5000</h2>

Example code and tutorial:  
* https://raspberrytips.nl/tcrt5000/  
* https://github.com/the-raspberry-pi-guy/robot  

<p align="center">
<img src="assets/TCRT5000.jpeg" width=300/><br>
Demo<br>
<img src="assets/TCRT5000_demo2.png" width=500/><br>
</p>

<h2 id="servo">Servo</h2>

* tutorial:  
    * Servo control: https://www.youtube.com/watch?v=N5QmZ92uvUo  
    * Servo platform installation: http://v.youku.com/v_show/id_XODk3NDE1NjYw.html  
    * 

<h2 id='HC-SR04'>HC-SR04 Ultrasonic Rangefinder</h2>

reference:  
* https://www.youtube.com/watch?v=sXJjfEisjpo  
* https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi  
* https://raspberrytips.nl/hc-sr04-ultrasone-sensor/  
* https://gist.github.com/raspberrytipsnl/85cb7807340bede2279b12f950aef5cb  
* https://stackoverflow.com/questions/45488233/controlling-continuous-servo-using-python-in-raspberry-pi-but-the-continuous-ser

<p align="center">
Circuit diagram<br>
<img src="assets/hc-sr04-tut-2.png" width=500/><br>
Implementation<br>
<img src="assets/HC-SR04-diagram1.JPG" width=500/><br>
<img src="assets/HC-SR04-diagram2.JPG" width=500 /><br>  
<img src="assets/HC-SR04-diagram3.JPG" width=500/><br>  
Demo<br>
<img src="assets/HC-SR04-diagram-demo.png" width=500/><br>  
</p>

<h2 id='Flask_Web_Server'>Flask Web Server</h2>

* https://randomnerdtutorials.com/raspberry-pi-web-server-using-flask-to-control-gpios/  
* http://mattrichardson.com/Raspberry-Pi-Flask/
* http://nessy.info/?p=1136
* http://vladikk.com/2013/09/12/serving-flask-with-nginx-on-ubuntu/  

Munually start web server:  
```shell
# launch mjpg streamer
cd ~/mjpg-streamer/mjpg-streamer/mjpg-streamer-experimental/
nohup ./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so -x 640 -y 480 -fps 20 -ex night -rot 0" &
# launch nginx
sudo /etc/init.d/nginx restart
# launch main control server
python3 ~/RC_car/src/web-server/server.py
```  

<h2 id="NRF24L01">NRF24L01</h2>

* http://thezanshow.com/electronics-tutorials/raspberry-pi/tutorial-32-33  
* https://github.com/BLavery/lib_nrf24  
* SPI and I2C tutorial: https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial

<h2 id='KY-037'>KY-037</h2>

reference:  
http://sensorkit.en.joy-it.net/index.php?title=KY-037_Microphone_sensor_module_(high_sensitivity)  
<img src="assets/KY-037.png" width=200/><br>

<h2 id='FC-04'>FC-04</h2>

reference:
http://www.instructables.com/id/Using-a-sound-sensor-with-a-Raspberry-Pi-to-contro/

<h2 id='sound'>Sound Detector</h2>

reference:  
https://www.youtube.com/watch?v=GiXNUYPrQ7I  

<h2 id='heart_rate'>Heart Rate module</h2>

* MCP3008 is required
* https://pulsesensor.com/
