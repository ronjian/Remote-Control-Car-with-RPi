# Steps to stream the Raspberry Pi camera video to client browser in the WIFI enviroment.
Refer to this post for detail: http://petrkout.com/electronics/low-latency-0-4-s-video-streaming-from-raspberry-pi-mjpeg-streamer-opencv/  
Do below steps on the Raspberry Pi (Mine is Raspberry Pi 3 Model B):  
```shell
mkdir mjpg-streamer
cd mjpg-streamer
git clone https://github.com/jacksonliam/mjpg-streamer.git .
cd mjpg-streamer-experimental
make
export LD_LIBRARY_PATH=.
./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so -x 640 -y 480 -fps 20 -ex night -rot 180"
```  
Check the browser via url ```http://r3:8080/?action=stream```, 
```r3``` is my Pi's hostname in the internel network, Ip address like ```192.168.31.110``` also works fine.  
### Demo:
<p align="center">
<img src="assets/infinite.png" width=700/>
<p/>