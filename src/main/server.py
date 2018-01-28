from flask import Flask, render_template
from flask import request
import motor
import servo
import ultrasonic


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/forward")
def forward():
    speed_pct = int(request.args.get('speed_pct'))
    motor_control.forward(speed_pct)
    return "OK"
 
@app.route("/backward")
def backward():
    speed_pct = int(request.args.get('speed_pct'))
    motor_control.backward(speed_pct)
    return "OK"

@app.route("/turn_left")
def turn_left():
    speed_pct = int(request.args.get('speed_pct'))
    motor_control.left(speed_pct)
    return "OK"
 
@app.route("/turn_right")
def turn_right():
    speed_pct = int(request.args.get('speed_pct'))
    motor_control.right(speed_pct)
    return "OK"

@app.route("/stop")
def stop():
    motor_control.stop()
    return "OK"

@app.route("/camera_up")
def camera_up():
    camera_vertical_servo.step_move(direction = -1.0)
    return "OK"
 
@app.route("/camera_down")
def camera_down():
    camera_vertical_servo.step_move(direction = 1.0)
    return "OK"

@app.route("/camera_left")
def camera_left():
    camera_horizontal_servo.step_move(direction = 1.0)
    return "OK"
 
@app.route("/camera_right")
def camera_right():
    camera_horizontal_servo.step_move(direction = -1.0)
    return "OK"

@app.route("/camera_reset")
def camera_reset():
    camera_vertical_servo.reset()
    camera_horizontal_servo.reset()
    return "OK"

@app.route("/take_photo")
def take_photo():
    pass
    return "OK"

@app.route("/back_uc_left")
def back_uc_left():
    back_servo.step_move(direction = 1.0)
    return "OK"
 
@app.route("/back_uc_right")
def back_uc_right():
    back_servo.step_move(direction = -1.0)
    return "OK"

@app.route("/back_uc_reset")
def back_uc_reset():
    back_servo.reset()
    return "OK"

@app.route("/back_distance")
def back_distance():
    print("Back distance is %f cm" % back_ultrasonic.detect())
    return "OK"

@app.route("/left_uc_left")
def left_uc_left():
    left_servo.step_move(direction = 1.0)
    return "OK"
 
@app.route("/left_uc_right")
def left_uc_right():
    left_servo.step_move(direction = -1.0)
    return "OK"

@app.route("/left_uc_reset")
def left_uc_reset():
    left_servo.reset()
    return "OK"

@app.route("/left_distance")
def left_distance():
    print("Left distance is %f cm" % left_ultrasonic.detect())
    return "OK"

@app.route("/right_uc_left")
def right_uc_left():
    right_servo.step_move(direction = 1.0)
    return "OK"
 
@app.route("/right_uc_right")
def right_uc_right():
    right_servo.step_move(direction = -1.0)
    return "OK"

@app.route("/right_uc_reset")
def right_uc_reset():
    right_servo.reset()
    return "OK"

@app.route("/right_distance")
def right_distance():
    print("Right distance is %f cm" % right_ultrasonic.detect())
    return "OK"

if __name__ == "__main__":
    try:
        motor_control = motor.CONTROL(RIGHT_FRONT_PIN=17, LEFT_FRONT_PIN=23, RIGHT_BACK_PIN=22, LEFT_BACK_PIN=24)

        camera_vertical_servo = servo.CONTROL(PIN=26)
        camera_horizontal_servo = servo.CONTROL(PIN=19)

        back_servo = servo.CONTROL(PIN=18)
        back_ultrasonic = ultrasonic.CONTROL(TRIG = 6, ECHO = 13)

        left_servo = servo.CONTROL(PIN=4)
        left_ultrasonic = ultrasonic.CONTROL(TRIG = 25, ECHO = 20)

        right_servo = servo.CONTROL(PIN=27)
        right_ultrasonic = ultrasonic.CONTROL(TRIG = 5, ECHO = 21)

        app.run(host='0.0.0.0', port=2000, debug=False)

    finally:
        print("Clearing")
        motor_control.close()
        camera_vertical_servo.close()
        camera_horizontal_servo.close()
        back_servo.close()
        back_ultrasonic.close()
        left_servo.close()
        left_ultrasonic.close()
        right_servo.close()
        right_ultrasonic.close()
        print("Bye!")

    