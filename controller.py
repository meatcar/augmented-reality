
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
    imu_measurements = {"acc" : [[],[],[]], "gyr" : [[],[],[]], "time" : [], "mag" : []}
    last_angles = [0, 0, 0]
    compass_bearing_filter = deque([])
    compass_bearing_filter_size = 10
    initial_angles = []

    total_angle = 0
    total_angle_old = 0
    pitch = 0
    pitch_old = 0
    first = -1000

    def __init__(self, head):
        self.phidget = PhidgetWrapper(self.on_data)
        self.head = head

        self.t = Thread(target=self.update_head)
        self.t.daemon = True
        self.t.start()

    def on_data(self, acc, gyr, mag, microseconds):
        Controller.imu_measurements["acc"][0].append(acc[0])
        Controller.imu_measurements["acc"][1].append(acc[1])
        Controller.imu_measurements["acc"][2].append(acc[2])

        Controller.imu_measurements["gyr"][0].append(gyr[0])
        Controller.imu_measurements["gyr"][1].append(gyr[1])
        Controller.imu_measurements["gyr"][2].append(gyr[2])

        Controller.imu_measurements["mag"].append(mag)
        Controller.imu_measurements["time"].append(microseconds)

    def process_data(self, acc, gyr, mag, del_t):
        # data is suppoed to be in chunks of 50
        delta = 2;

        z = np.mean(acc[0])
        x = np.mean(acc[1])
        y = np.mean(acc[2])

        gravity = [x,y,z]

        z = np.mean(gyr[0][1:])

        # 50 samples accumulate every 0.2 seconds.
        if abs(z) > 0.8:
            self.total_angle = self.total_angle + z*0.2;

        rollAngle = math.atan2(gravity[1], gravity[2]);
        pitchAngle = math.atan(-gravity[0]/((gravity[1]*math.sin(rollAngle)) + (gravity[2] * math.cos(rollAngle))));

        r = 30*math.pi/180.0 * 100

        if self.first == -1000:
            self.first = round(pitchAngle*r,1);

        self.pitch = round(pitchAngle*r,1)-self.first;


        p = self.pitch
        po = self.pitch_old

        a = self.total_angle
        ao = self.total_angle_old

        if abs(p-po) > delta and abs(a-ao) < delta:
            self.total_angle = ao;
            self.pitch_old = p
        elif abs(p-po) < delta and abs(a-ao) > delta:
            self.total_angle_old = a;
            self.pitch = po;
        elif abs(p-po) < delta and abs(p-po) < delta:
            self.total_angle = ao;
            self.pitch = po;

        self.head.xangle = 0;
        self.head.yangle = (-2)*math.radians(self.total_angle) - math.radians(45) # on xy plane for gl;
        self.head.zangle = math.radians(self.pitch) # on zx plane for gl;
 
    def update_head(self):
        while True:
            if len(Controller.imu_measurements["acc"][0]) >= 50:
                data = copy(Controller.imu_measurements)
                self.process_data(data["acc"], data["gyr"], data["mag"], None);
                Controller.imu_measurements = {"acc" : [[],[],[]], "gyr" : [[],[],[]], "time" : [], "mag" : []}

if __name__ == "__main__":
    h = Head()
    c = Controller(h)

    while True:
        time.sleep(0.02)
        print(h)
