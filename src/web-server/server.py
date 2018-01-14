from flask import Flask, render_template
from motor import motor_control 
from servo import camera_control
from servo import ultrasonic_control
from flask import request

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

if __name__ == "__main__":
    mc = motor_control.CONTROL(Frequency=300)
    cc = camera_control.CONTROL(STRIDE= 0.1)
    back_uc = ultrasonic_control.CONTROL(STRIDE= 0.1, PIN=18)
    app.run(host='0.0.0.0', port=2000, debug=False)