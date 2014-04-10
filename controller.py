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
from mpuwrapper import MPUWrapper

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
    
    # mpu measurements
    # 
    # the calibrated measurements have been passed through a low pass filter.
    # 
    # l_acc - linear accleration data
    # r_acc - raw acceleration data
    # r_gyr - raw gyro data
    # r_mag - raw magnetic data
    # c_acc - calibrated acceleration data
    # c_mag - calibrated magnetic data
    # e_ang - Euler angles with reference to the earth frame
    # r_quat - the raw quaternion
    # c_quat - calculated quaternion
    # fe_ang - fused euler pose.
    # res_acc ` residual acceleration (supposed to be tilt compensated.)
    mpu_measurements = {"l_acc": [],
        "r_acc" : [], "r_gyr" : [], "r_mag" : [],
        "c_acc" : [], "c_mag" : [], 
        "e_ang" : [], "fe_ang" : [], 
        "c_quat" : [], "r_quat" : [],
        "res_acc" : [] }

    def __init__(self, head, use_phidget=False, use_MPU=True, device="/dev/ttyACM0", speed=115200):
        self.use_phidget = use_phidget
        self.use_MPU = use_MPU

        if use_phidget:
            self.phidget = PhidgetWrapper(self.on_phidget_data)
    
        if use_MPU:
            self.mpu = MPUWrapper(device, speed, self.on_mpu_data)

        self.head = head

        self.t = Thread(target=self.update_head)
        self.t.daemon = True
        self.t.start()

    def on_phidget_data(self, acc, gyr, mag, microseconds):
        Controller.imu_measurements["acc"].append(acc)
        Controller.imu_measurements["gyr"].append(gyr)
        Controller.imu_measurements["mag"].append(mag)
        Controller.imu_measurements["time"].append(microseconds)

    def on_mpu_data(self, l_acc, r_acc, r_gyr, r_mag, c_acc, c_mag, e_ang, 
        r_quat, c_quat, fe_ang, res_acc):
        Controller.mpu_measurements["l_acc"].append(l_acc);
        Controller.mpu_measurements["r_acc"].append(r_acc);
        Controller.mpu_measurements["r_gyr"].append(r_gyr);
        Controller.mpu_measurements["r_mag"].append(r_mag);
        Controller.mpu_measurements["c_acc"].append(l_acc);
        Controller.mpu_measurements["c_mag"].append(c_mag);
        Controller.mpu_measurements["e_ang"].append(e_ang);
        Controller.mpu_measurements["r_quat"].append(r_quat);
        Controller.mpu_measurements["c_quat"].append(c_quat);
        Controller.mpu_measurements["fe_ang"].append(fe_ang);
        Controller.mpu_measurements["res_acc"].append(res_acc);

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
            if self.use_MPU and not self.use_phidget:
                if len(Controller.mpu_measurements["fe_ang"]) > 0:
                    angles = Controller.mpu_measurements["fe_ang"][-1]
                    print(angles)
                    self.head.xangle = math.radians(angles[0])
                    self.head.yangle = math.radians(angles[1])
                    self.head.zangle = math.radians(angles[2]) - math.radians(0)

            elif self.use_phidget and not self.use_MPU:
                if len(Controller.imu_measurements["acc"]) >= 6:
                    data = copy(Controller.imu_measurements)
                    self.process_data(data["acc"], data["gyr"], data["mag"], None);
                    Controller.imu_measurements["acc"] = Controller.imu_measurements["acc"][1:]
                    Controller.imu_measurements["gyr"] = Controller.imu_measurements["gyr"][1:]
                    Controller.imu_measurements["mag"] = Controller.imu_measurements["mag"][1:]
                    Controller.imu_measurements["time"] = Controller.imu_measurements["time"][1:]
            elif self.use_phidget and self.use_MPU:
                print("ok")

# if __name__ == "__main__":
    # head = Head()
    # c = Controller(head)

    # while True:
    #     x_a = head.xangle
    #     y_a = head.yangle
    #     z_a = head.zangle

    #     print x_a
    #     print y_a
    #     print z_a
    #     print ""
    #     R_x = np.matrix([[1,0,0],[0,math.cos(x_a),math.sin(x_a)],[0,-math.sin(x_a),math.cos(x_a)]])
    #     R_y = np.matrix([[math.cos(y_a),0,-math.sin(y_a)],[0,1,0],[math.sin(y_a),0,math.cos(y_a)]])
    #     R_z = np.matrix([[math.cos(z_a),math.sin(z_a),0],[-math.sin(z_a),math.cos(z_a),0],[0,0,1]])
    #     v = R_x*R_y*R_z*np.matrix([[1],[0],[0]]);
    #     print v

    #     time.sleep(1);
