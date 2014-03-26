#!/bin/python

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

    heading = 0
    heading_old = 0

    pitch = 0
    pitch_old = 0

    roll = 0
    roll_old = 10

    # stores roll pitch yaw initial values.
    first = [-1000, -1000, -1000]
    imu_measurements = {"acc" : [], "gyr" : [], "mag" : [], "time" : []}

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
        delta = 2;

        # n x 3 matrix.
        acc = np.matrix(acc)

        # n x 3 matrix.
        gyr = np.matrix(gyr)

        # mean acceleration per axis for this data window.
        acc_z = np.mean(acc[0:,0])
        acc_x = np.mean(acc[0:,1])
        acc_y = np.mean(acc[0:,2])

        # mean gyro reading in the x axis.
        # this is used to compute the heading (YAW).
        #
        # ignore the first value in gyro data, and take the mean to apply
        # simple filtering.
        # TODO: try better smoothing techniques
        # - exponential smoothing,
        # - moving average
        #
        # TODO: need to compensate for drift.
        gyr_z = np.mean(gyr[1:,0])

        # gravity measured by acceleration due to gravity.
        gravity = [acc_x, acc_y, acc_z]

        # 12 samples accumulate about every 0.05 seconds.
        # compute to total change in YAW by integrating points over time.
        #
        # TOOD: The current implementation uses a simple filtering of the
        # gyro data. A threshold of 0.8 is chosen. Only is the angular
        # rate of change is greater than the threshold, will there be
        # a change in the total angle.
        if abs(gyr_z) > 0.8:
            self.heading = self.heading + gyr_z*0.025;

        # Compute the pitch and roll using formula's on the phidgets website.
        roll_angle = math.atan2(gravity[1], gravity[2]);
        pitch_angle = math.atan(-gravity[0]/((gravity[1]*math.sin(roll_angle)) + (gravity[2] * math.cos(roll_angle))));

        # Scaling factor for producing reasonable degree numbers.
        r = 30*math.pi/180.0 * 100

        # record the first value as a threshold.
        # All the values after will be adjusted based on this.
        if self.first[0] == -1000:
            self.first = [0, 0, 0]
            self.first[0] = roll_angle;
            self.first[1] = round(pitch_angle*r,1);
            self.first[2] = 0

        # compute the current pitch
        self.pitch = round(pitch_angle*r,1)  - self.first[1];
        # self.roll = roll_angle - self.first[0]

        # self.roll = self.roll * 0.025

        # The following code compensates for simultaneous movements in
        # pitch and YAW which would lead to incorrect measurement of
        # angles in both movements.

        _pitch     = self.pitch
        _pitch_old = self.pitch_old

        _heading = self.heading
        _heading_old = self.heading_old

        _roll = self.roll
        _roll_old = self.roll_old

        # print self.roll

        # print abs(_roll - _roll_old)

        # Only update roll angle if the difference is more than 0.1
        # if abs(_roll - _roll_old) < 0.15:
        #     self.roll_old = self.roll

        # If changes in heading are small but changes in pitch are significant
        # only update the pitch.
        if  abs(_pitch - _pitch_old) > delta and abs(_heading - _heading_old) < delta:
            self.heading = _heading_old
            self.pitch_old = _pitch

        # If changes in pitch are small but changes in heading are significant
        # only update the heading.
        if abs(_pitch - _pitch_old) < delta and abs(_heading - _heading_old) > delta:
            self.heading_old = _heading;
            self.pitch = _pitch_old;

        # If changes in pitch and heading are less than delta, then ignore the
        # changes for both.
        if abs(_pitch - _pitch_old) < delta and abs(_heading - _heading_old) < delta:
            self.heading = _heading_old;
            self.pitch = _pitch_old;

        self.head.xangle = 0;
        self.head.yangle = (-1)*math.radians(self.heading) - math.radians(45) # on xy plane for gl;
        self.head.zangle = (1)*math.radians(self.pitch) # on zx plane for gl;

    def update_head(self):
        while True:
            if len(Controller.imu_measurements["acc"]) >= 6:
                data = copy(Controller.imu_measurements)
                self.process_data(data["acc"], data["gyr"], data["mag"], None);
                Controller.imu_measurements["acc"] = Controller.imu_measurements["acc"][1:]
                Controller.imu_measurements["gyr"] = Controller.imu_measurements["gyr"][1:]
                Controller.imu_measurements["mag"] = Controller.imu_measurements["mag"][1:]
                Controller.imu_measurements["time"] = Controller.imu_measurements["time"][1:]

if __name__ == "__main__":
    h = Head()
    c = Controller(h)

    while True:
        time.sleep(1);
        print(h)
