from motor import motor_control
from servo import ultrasonic_control
from HC_SR04 import ultrasonic_distance
from MH_FMD import alert
from time import sleep
from time import time
import io

class Obstacle_avoidance:
	def __init__(self):
		self.mc = motor_control.CONTROL(Frequency=300)
		self.left_uc = ultrasonic_control.CONTROL(STRIDE= 0.1, PIN=4, NOMINAL=7.5)
		self.right_uc = ultrasonic_control.CONTROL(STRIDE= 0.1, PIN=27, NOMINAL=7.5)
		self.left_ud = ultrasonic_distance.UltrasonicSensor(TRIG = 25, ECHO = 20)
		self.right_ud = ultrasonic_distance.UltrasonicSensor(TRIG = 5, ECHO = 21)
		self.front_ud = ultrasonic_distance.UltrasonicSensor(TRIG = 16, ECHO = 12)
		self.alert = alert.Alert(PIN=6)

	def uc_move(self, uc, direction=1.0):
		uc.reset()
		uc.horizontal_move(direction)

	def uc_to(self, uc, pos):
		uc.horizontal_pos(pos)
		sleep(0.1)

	def avg_distance(self,  ud):
		record = []
		for i in range(3):
			record.append(ud.detect())
			sleep(0.01)
		record.sort()
		dis=record[1]
		return dis

	def tune_servo(self, uc):
		front_done=False
		front_pos = 0.0
		while not front_done :
			self.uc_to(uc, front_pos)
			input_txt = input("now front position is %f, enter number to tune or enter to done: " % front_pos)
			if input_txt == "": 
				front_done = True
			else :
				front_pos = float(input_txt)

		side_done=False
		side_pos = 0.0
		while not side_done :
			self.uc_to(uc, side_pos)
			input_txt = input("now side position is %f, enter number to tune or enter to done: " % side_pos)
			if input_txt == "": 
				side_done = True
			else :
				side_pos = float(input_txt)
		return front_pos, side_pos

	def uc_scan(self, uc, ud, front, side):
		# from front to side
		min_dis = 400 # start at max limitation
		ref_pos = 0.0
		step = (side - front) / 10.0
		pos = front
		while (front <= pos and pos <= side ) or (front >= pos and pos >= side ):
			pos += step
			self.uc_to(uc, pos)
			dis = self.avg_distance(ud)
			if dis < min_dis:
				min_dis = dis
				ref_pos = pos
		self.uc_to(uc, ref_pos)
		return min_dis , ref_pos



if __name__ == "__main__":
	core = Obstacle_avoidance()
	LEFT_FRONT_DC, LEFT_SIDE_DC =   5.5, 11.0 #core.tune_servo(core.left_uc)
	RIGHT_FRONT_DC, RIGHT_SIDE_DC =   10.0, 4.5 #core.tune_servo(core.right_uc)
	side_threshold=15 # cm
	front_threshold=20 # cm
	action_list = [] # structure: [(timestamp, action)]
	try:
		forward=False
		turn_flag="left"
		while True:
			#seek path
			if forward==False:
				left_danger, left_ref_pos = core.uc_scan(core.left_uc, core.left_ud, LEFT_FRONT_DC, LEFT_SIDE_DC)
				print("left min distance is %f cm , at %f dc position" % (left_danger, left_ref_pos) )
				right_danger, right_ref_pos = core.uc_scan(core.right_uc, core.right_ud, RIGHT_FRONT_DC, RIGHT_SIDE_DC)
				print("right min distance is %f cm , at %f dc position" % (right_danger, right_ref_pos))
				front_danger = core.avg_distance(core.front_ud)
				print("front danger is %f cm " % front_danger)
				if right_danger > side_threshold and left_danger > side_threshold and front_danger>front_threshold:
					print("Go!")
					action_list.append((time(), "forward"))
					core.mc.forward(30)
					forward=True
				else:
					if left_danger < 5 and turn_flag == "left" :
						turn_flag = "right"
					elif right_danger < 5 and turn_flag == "right" :
						turn_flag = "left"

					if turn_flag == "left":
						print("turn left")
						action_list.append((time(), "left"))
						core.mc.left(60)
						sleep(0.2)
						core.mc.stop()
					else:
						print("turn right")
						action_list.append((time(), "right"))
						core.mc.right(60)
						sleep(0.2)
						core.mc.stop()
			#monitor danger
			else:
				left_danger = core.avg_distance(core.left_ud)
				right_danger = core.avg_distance(core.right_ud)
				front_danger = core.avg_distance(core.front_ud)
				if left_danger < side_threshold or right_danger < side_threshold or front_danger < front_threshold:
						print("Stop!")
						action_list.append((time(), "stop"))
						core.mc.stop()
						forward=False
	except KeyboardInterrupt:
		print("cancelled")
	finally:
		#write action list into file:
		with io.open(file='action_list.txt', mode='w', encoding='utf-8') as f:
			for x in action_list:
				f.write(str(x)+"\n")
		print("bye!")