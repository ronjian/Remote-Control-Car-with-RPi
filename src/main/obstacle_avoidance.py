import motor
import servo
import ultrasonic
from time import sleep
from pathlib import Path

def __uc_to( uc, pos):
	uc.direct_move(pos)
	sleep(0.3)

def __avg_distance(  ud):
	record = []
	for i in range(3):
		record.append(ud.detect())
		sleep(0.01)
	record.sort()
	dis=record[1]
	return dis

def __tune_servo( uc):
	front_done=False
	front_pos = 0.0
	while not front_done :
		__uc_to(uc, front_pos)
		input_txt = input("now front position is %f, enter number to tune or enter to done: " % front_pos)
		if input_txt == "": 
			front_done = True
		else :
			front_pos = float(input_txt)
	side_done=False
	side_pos = 0.0
	while not side_done :
		__uc_to(uc, side_pos)
		input_txt = input("now side position is %f, enter number to tune or enter to done: " % side_pos)
		if input_txt == "": 
			side_done = True
		else :
			side_pos = float(input_txt)
	return front_pos, side_pos

def __uc_scan( uc, ud, front, side):
	# from front to side
	min_dis = 400 # start at max limitation
	step = (side - front) / 10.0
	pos = front
	while (front <= pos and pos <= side ) or (front >= pos and pos >= side ):
		pos += step
		__uc_to(uc, pos)
		dis = __avg_distance(ud)
		if dis < min_dis:
			min_dis = dis
			ref_pos = pos
	__uc_to(uc, ref_pos)
	return min_dis , ref_pos

def start():
	oa_signal_path = Path('assets/obstacle_avoidance_exit.signal')
	# kick off all instances
	# motor control
	mc = motor.CONTROL(RIGHT_FRONT_PIN=17, 
						LEFT_FRONT_PIN=23, 
						RIGHT_BACK_PIN=22, 
						LEFT_BACK_PIN=24)
	# left servo
	left_uc = servo.CONTROL(PIN=4)
	# right servo
	right_uc = servo.CONTROL(PIN=27)
	# left ultrasonic
	left_ud = ultrasonic.CONTROL(TRIG = 25, ECHO = 20)
	# right ultrasonic
	right_ud = ultrasonic.CONTROL(TRIG = 5, ECHO = 21)
	# front ultrasonic
	front_ud = ultrasonic.CONTROL(TRIG = 16, ECHO = 12)

	LEFT_FRONT_DC, LEFT_SIDE_DC =   5.5, 11.0 # tune_servo(left_uc)
	RIGHT_FRONT_DC, RIGHT_SIDE_DC =   10.0, 4.5 # tune_servo(right_uc)
	side_threshold=20 # cm
	front_threshold=30 # cm
	turn_threshold = 6 # cm
	speed = 60
	try:
		forward=False
		turn_flag="left"
		while True:
			# seek path
			if forward==False:
				# check exit signal
				if oa_signal_path.exists():
					break
				else:
					left_danger, left_ref_pos = __uc_scan(left_uc, left_ud, LEFT_FRONT_DC, LEFT_SIDE_DC)
					print("left min distance is %f cm" % left_danger )
					right_danger, right_ref_pos = __uc_scan(right_uc, right_ud, RIGHT_FRONT_DC, RIGHT_SIDE_DC)
					print("right min distance is %f cm" % right_danger)
					front_danger = __avg_distance(front_ud)
					print("front danger is %f cm " % front_danger)
					if right_danger > side_threshold and left_danger > side_threshold and front_danger>front_threshold:
						print("Go!")
						mc.forward(speed)
						forward=True
					else:
						if left_danger < turn_threshold and turn_flag == "left" :
							turn_flag = "right"
						elif right_danger < turn_threshold and turn_flag == "right" :
							turn_flag = "left"

						if turn_flag == "left":
							print("turn left")
							mc.left(speed)
							sleep(0.3)
							mc.stop()
						else:
							print("turn right")
							mc.right(speed)
							sleep(0.3)
							mc.stop()
			# monitor danger
			else:
				left_danger = __avg_distance(left_ud)
				right_danger = __avg_distance(right_ud)
				front_danger = __avg_distance(front_ud)
				if left_danger < side_threshold or right_danger < side_threshold or front_danger < front_threshold:
						print("Stop!")
						mc.stop()
						forward=False
				sleep(0.01)
	except Exception as e:
		print(str(e))
	finally:
		# clear
		left_uc.close()
		right_uc.close()
		mc.close()
		left_ud.close()
		right_ud.close()
		front_ud.close()
		if oa_signal_path.exists():oa_signal_path.unlink()
		print("exit obstacle avoidance mode")

if __name__ == "__main__":
	start()

