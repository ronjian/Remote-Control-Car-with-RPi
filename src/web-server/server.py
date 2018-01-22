from flask import Flask, render_template
from flask import request
from motor import motor_control 
from servo import camera_control
from servo import ultrasonic_control
from HC_SR04 import ultrasonic_distance


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/forward")
def forward():
    speed_pct = int(request.args.get('speed_pct'))
    mc.forward(speed_pct)
    return "OK"
 
@app.route("/backward")
def backward():
    speed_pct = int(request.args.get('speed_pct'))
    mc.backward(speed_pct)
    return "OK"

@app.route("/turn_left")
def turn_left():
    speed_pct = int(request.args.get('speed_pct'))
    mc.left(speed_pct)
    return "OK"
 
@app.route("/turn_right")
def turn_right():
    speed_pct = int(request.args.get('speed_pct'))
    mc.right(speed_pct)
    return "OK"

@app.route("/stop")
def stop():
    mc.stop()
    return "OK"

@app.route("/camera_up")
def camera_up():
    cc.horizontal_move(direction = -1.0)
    return "OK"
 
@app.route("/camera_down")
def camera_down():
    cc.horizontal_move(direction = 1.0)
    return "OK"

@app.route("/camera_left")
def camera_left():
    cc.vertical_move(direction = 1.0)
    return "OK"
 
@app.route("/camera_right")
def camera_right():
    cc.vertical_move(direction = -1.0)
    return "OK"

@app.route("/camera_reset")
def camera_reset():
    cc.reset()
    return "OK"

@app.route("/take_photo")
def take_photo():
    camera.take_photo()
    return "OK"

@app.route("/back_uc_left")
def back_uc_left():
    back_uc.horizontal_move(direction = 1.0)
    return "OK"
 
@app.route("/back_uc_right")
def back_uc_right():
    back_uc.horizontal_move(direction = -1.0)
    return "OK"

@app.route("/back_uc_reset")
def back_uc_reset():
    back_uc.reset()
    return "OK"

@app.route("/back_distance")
def back_distance():
    print("Back distance is %f cm" % back_ud.detect())
    return "OK"

@app.route("/left_uc_left")
def left_uc_left():
    left_uc.horizontal_move(direction = 1.0)
    return "OK"
 
@app.route("/left_uc_right")
def left_uc_right():
    left_uc.horizontal_move(direction = -1.0)
    return "OK"

@app.route("/left_uc_reset")
def left_uc_reset():
    left_uc.reset()
    return "OK"

@app.route("/left_distance")
def left_distance():
    print("Left distance is %f cm" % left_ud.detect())
    return "OK"

@app.route("/right_uc_left")
def right_uc_left():
    right_uc.horizontal_move(direction = 1.0)
    return "OK"
 
@app.route("/right_uc_right")
def right_uc_right():
    right_uc.horizontal_move(direction = -1.0)
    return "OK"

@app.route("/right_uc_reset")
def right_uc_reset():
    right_uc.reset()
    return "OK"

@app.route("/right_distance")
def right_distance():
    print("Right distance is %f cm" % right_ud.detect())
    return "OK"

if __name__ == "__main__":
    mc = motor_control.CONTROL(Frequency=300)
    cc = camera_control.CONTROL(STRIDE= 0.1)
    back_uc = ultrasonic_control.CONTROL(STRIDE= 0.1, PIN=18)
    back_ud = ultrasonic_distance.UltrasonicSensor(TRIG = 16, ECHO = 12)
    left_uc = ultrasonic_control.CONTROL(STRIDE= 0.1, PIN=4)
    right_uc = ultrasonic_control.CONTROL(STRIDE= 0.1, PIN=27)
    left_ud = ultrasonic_distance.UltrasonicSensor(TRIG = 25, ECHO = 20)
    right_ud = ultrasonic_distance.UltrasonicSensor(TRIG = 5, ECHO = 21)

    app.run(host='0.0.0.0', port=2000, debug=False)