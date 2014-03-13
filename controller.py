
import sys
import time
import copy
import math
import numpy as np

from copy import copy
from head import Head
from threading import Thread
from collections import deque
from phidgetwrapper import PhidgetWrapper

class Controller(object):
    head = None
    imu_measurements = {"acc" : [], "gyr" : [], "time" : [], "mag" : []}
    initial_angles = []
    last_angles = [0, 0, 0]
    compass_bearing_filter = deque([])
    compass_bearing_filter_size = 10
    initial_angles_threshold = 50

    def __init__(self, head):
        self.phidget = PhidgetWrapper(self.on_data)
        self.head = head

        self.t = Thread(target=self.update_head)
        self.t.daemon = True
        self.t.start()

    def on_data(self, acc, gyr, mag, microseconds):
        Controller.imu_measurements["acc"].append(acc)
        Controller.imu_measurements["gyr"].append(gyr)
        Controller.imu_measurements["mag"].append(mag)
        Controller.imu_measurements["time"].append(microseconds)

    def process_data(self, acc, gyr, mag, del_t):
        n = min(len(acc), len(mag))
        r = (180.0/math.pi); # 1 radian.

        for i in range(n):
            gravity = [acc[i][0], acc[i][1], acc[i][2]];
            mag_field = [mag[i][0], mag[i][1], mag[i][2]];

            roll_angle = math.atan2(gravity[1], gravity[2]);
            pitch_angle = math.atan(-gravity[0]/((gravity[1]*math.sin(roll_angle)) + (gravity[2] * math.cos(roll_angle))));
            yaw_angle = math.atan2((mag_field[2]*math.sin(roll_angle))-(mag_field[1]*math.cos(roll_angle)),
                (mag_field[0]*math.cos(pitch_angle))+(mag_field[1]*math.sin(pitch_angle)*math.sin(roll_angle))+(mag_field[2]*math.sin(pitch_angle)*math.cos(roll_angle)));

            angles = [roll_angle, pitch_angle, yaw_angle];
            deg_angels = [yaw_angle*r, pitch_angle*r, roll_angle*r];

            # if Controller.initial_angles != []:
            #     deg_angels = [yaw_angle*r - Controller.initial_angles[0], pitch_angle*r - Controller.initial_angles[1], roll_angle*r-Controller.initial_angles[2]];

            # print deg_angels;

            # Low pass filter.
            for i in list([0,1,2]):
                if abs(angles[i] - self.last_angles[i]) > 3:
                    for compass_bearing in self.compass_bearing_filter:
                        if angles[i] > self.last_angles[i]: 
                            compass_bearing[i] += 360 * r;
                        else:
                            compass_bearing[i] -= 360 * r;

            self.last_angles = copy(angles);

            self.compass_bearing_filter.append(copy(angles));

            if self.compass_bearing_filter.__len__() > self.compass_bearing_filter_size:
                self.compass_bearing_filter.reverse();
                self.compass_bearing_filter.pop();
                self.compass_bearing_filter.reverse();

            yaw_angle = pitch_angle = roll_angle = 0;

            for compass_bearing in self.compass_bearing_filter:
                roll_angle += compass_bearing[0];
                pitch_angle += compass_bearing[1];
                yaw_angle += compass_bearing[2];

            l = float(self.compass_bearing_filter.__len__())

            yaw_angle /= l
            pitch_angle /= l
            roll_angle /= l
            yaw_angle_deg = yaw_angle * r;
            pitch_angle_deg = pitch_angle * r
            roll_angle_deg = roll_angle * r

            if len(Controller.initial_angles) < Controller.initial_angles_threshold:
                Controller.initial_angles.append([pitch_angle_deg, roll_angle_deg, yaw_angle_deg])
            else:
                init_pitch = 0
                init_roll = 0
                init_yaw = 0

                for ia in Controller.initial_angles:
                    init_pitch += ia[0]
                    init_roll += ia[1]
                    init_yaw += ia[2]

                init_pitch /= Controller.initial_angles_threshold    
                init_roll /= Controller.initial_angles_threshold
                init_yaw /= Controller.initial_angles_threshold

                self.head.xangle = 0
                self.head.yangle = 0
                # self.head.xangle = pitch_angle_deg - init_pitch
                # self.head.yangle = roll_angle_deg - init_roll
                if yaw_angle_deg - init_yaw < 100:
                    self.head.zangle = yaw_angle_deg - init_yaw

    def update_head(self):
        while True:
            data = copy(Controller.imu_measurements)
            self.process_data(data["acc"], data["gyr"], data["mag"], None);
            Controller.imu_measurements = {"acc" : [], "gyr" : [], "time" : [], "mag" : []}    

if __name__ == "__main__":
    h = Head()
    c = Controller(h)

    while True:
        time.sleep(1)
        print(h)
