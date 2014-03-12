"""


"""

from head import Head

# misc imports.
import sys
import time
import copy
import math
from threading import Thread

# imports for processing IMU data.
import numpy as np
from MahonyAHRS import MahonyAHRS
from QuaternionLibrary import QuaternionLibrary
from scipy.signal import butter, filtfilt

from LinearKalmanFilter import KalmanFilterLinear

from phidgetwrapper import PhidgetWrapper

class Controller(object):
    """

    """

    head = None
    # map axes strings to/from tuples of inner axis, parity, repetition, frame
    _AXES2TUPLE = {
        'sxyz': (0, 0, 0, 0), 'sxyx': (0, 0, 1, 0), 'sxzy': (0, 1, 0, 0),
        'sxzx': (0, 1, 1, 0), 'syzx': (1, 0, 0, 0), 'syzy': (1, 0, 1, 0),
        'syxz': (1, 1, 0, 0), 'syxy': (1, 1, 1, 0), 'szxy': (2, 0, 0, 0),
        'szxz': (2, 0, 1, 0), 'szyx': (2, 1, 0, 0), 'szyz': (2, 1, 1, 0),
        'rzyx': (0, 0, 0, 1), 'rxyx': (0, 0, 1, 1), 'ryzx': (0, 1, 0, 1),
        'rxzx': (0, 1, 1, 1), 'rxzy': (1, 0, 0, 1), 'ryzy': (1, 0, 1, 1),
        'rzxy': (1, 1, 0, 1), 'ryxy': (1, 1, 1, 1), 'ryxz': (2, 0, 0, 1),
        'rzxz': (2, 0, 1, 1), 'rxyz': (2, 1, 0, 1), 'rzyz': (2, 1, 1, 1)}

    _TUPLE2AXES = dict((v, k) for k, v in _AXES2TUPLE.items())

    _NEXT_AXIS = [1, 2, 0, 1]
    _EPS = np.finfo(float).eps * 4.0

    # stores acceleration, angular change and time delta.
    imu_measurements = {"acc" : [], "gyr" : [], "time" : []}

    def __init__(self, head):
        """

        """
        self.phidget = PhidgetWrapper(self.on_data)

        # head contains reference to object that is updated on every
        # update from the IMU.
        self.head = head

        self.t = Thread(target=self.update_head)
        self.t.daemon = True
        self.t.start()

    def on_data(self, acc, agr, microseconds):
        Controller.imu_measurements["acc"].append(acc)
        Controller.imu_measurements["gyr"].append(agr)
        Controller.imu_measurements["time"].append(microseconds)

    def euler_from_matrix(self, matrix, axes='sxyz'):
        """Return Euler angles from rotation matrix for specified axis sequence.

        axes : One of 24 axis sequences as string or encoded tuple

        Note that many Euler angle triplets can describe one matrix.

        >>> R0 = euler_matrix(1, 2, 3, 'syxz')
        >>> al, be, ga = euler_from_matrix(R0, 'syxz')
        >>> R1 = euler_matrix(al, be, ga, 'syxz')
        >>> numpy.allclose(R0, R1)
        True
        >>> angles = (4*math.pi) * (numpy.random.random(3) - 0.5)
        >>> for axes in _AXES2TUPLE.keys():
        ...    R0 = euler_matrix(axes=axes, *angles)
        ...    R1 = euler_matrix(axes=axes, *euler_from_matrix(R0, axes))
        ...    if not numpy.allclose(R0, R1): print(axes, "failed")

        """
        try:
            firstaxis, parity, repetition, frame = self._AXES2TUPLE[axes.lower()]
        except (AttributeError, KeyError):
            self._TUPLE2AXES[axes]  # validation
            firstaxis, parity, repetition, frame = axes

        i = firstaxis
        j = self._NEXT_AXIS[i+parity]
        k = self._NEXT_AXIS[i-parity+1]

        M = np.array(matrix, dtype=np.float64, copy=False)[:3, :3]
        if repetition:
            sy = math.sqrt(M[i, j]*M[i, j] + M[i, k]*M[i, k])
            if sy > self._EPS:
                ax = math.atan2( M[i, j],  M[i, k])
                ay = math.atan2( sy,       M[i, i])
                az = math.atan2( M[j, i], -M[k, i])
            else:
                ax = math.atan2(-M[j, k],  M[j, j])
                ay = math.atan2( sy,       M[i, i])
                az = 0.0
        else:
            cy = math.sqrt(M[i, i]*M[i, i] + M[j, i]*M[j, i])
            if cy > self._EPS:
                ax = math.atan2( M[k, j],  M[k, k])
                ay = math.atan2(-M[k, i],  cy)
                az = math.atan2( M[j, i],  M[i, i])
            else:
                ax = math.atan2(-M[j, k],  M[j, j])
                ay = math.atan2(-M[k, i],  cy)
                az = 0.0

        if parity:
            ax, ay, az = -ax, -ay, -az
        if frame:
            ax, az = az, ax
        return ax, ay, az

    def process_data(self, acc, gyr, del_t):
        """

        """

        samplePeriod = 1/256.0
        #samplePeriod = 4/1000.0

        # number of observations.
        N = len(acc)

        # process the data through the ARHS algorithm which will compute the
        # orientation.

        # contains a rotation matrix corresponding to each of the data points
        rotation_matrices = list()
        ahrs = MahonyAHRS('SamplePeriod', samplePeriod, 'Kp', 1)
        ql = QuaternionLibrary()

        for i in range(0, N):
            ahrs.UpdateIMU(np.array(gyr[i])*(np.pi/180), acc[i], ql.quaternProd)
            rotation_matrices.append(ql.quatern2rotMat(ahrs.Quaternion))

        # compute the tilt compensated acceleration.
        # this stores a list of numpy matrices, as col vectors.
        tcAcc = list()

        for i in range(0, N):
            R_i = rotation_matrices[i]
            acc_i = np.matrix(acc[i]).T
            tcAcc.append(R_i * (acc_i))

        # calculate the linear acceleration in Earth frame (subtracting gravity)
        linAcc = list()

        for i in range(0, N):
            linAcc.append(tcAcc[i] - np.matrix([0,0,1]).T)
            linAcc[i] = linAcc[i] * 9.81

        # calculate linear velocity (integrate acceleration)
        linVel = list()
        linVel.append(np.matrix([0,0,0]).T)

        for i in range(1, N):
            linVel.append(linVel[i - 1] + linAcc[i] * samplePeriod)

        # apply the high pass filter to linear velocity to remove drift
        order = 1
        filtCutOff = 0.1
        [b, a] = butter(order, (2*filtCutOff)/(1/0.01), 'high')

        x_vector = list()
        y_vector = list()
        z_vector = list()

        for i in range(0, N):
            x_vector.append(linVel[i][0,0])
            y_vector.append(linVel[i][1,0])
            z_vector.append(linVel[i][2,0])

        linVelHP_x = filtfilt(b, a, x_vector)
        linVelHP_y = filtfilt(b, a, y_vector)
        linVelHP_z = filtfilt(b, a, z_vector)

        # this contains a list of (numpy) col vectors.
        linVelHP = list()

        for i in range(0, N):
            linVelHP.append(np.matrix([linVelHP_x[i], linVelHP_y[i], \
                linVelHP_z[i]]).T)

        # calculate linear position (integrate velocity)
        linPos = list()
        linPos.append(np.matrix([0,0,0]).T)

        for i in range(1, N):
            linPos.append(linPos[i - 1] + linVelHP[i] * samplePeriod)

        # apply the high pass filter to linear position to remove drift
        order = 1
        filtCutOff = 0.1
        [b, a] = butter(order, (2*filtCutOff)/(1/0.01), 'high')

        x_vector = list()
        y_vector = list()
        z_vector = list()

        for i in range(0, N):
            x_vector.append(linPos[i][0,0])
            y_vector.append(linPos[i][1,0])
            z_vector.append(linPos[i][2,0])

        linPosHP_x = filtfilt(b, a, x_vector)
        linPosHP_y = filtfilt(b, a, y_vector)
        linPosHP_z = filtfilt(b, a, z_vector)

        linPosHP = list()

        for i in range(0, N):
            linPosHP.append(np.matrix([linPosHP_x[i], linPosHP_y[i], \
                linPosHP_z[i]]).T)

        for i in range(N-1, N):
            x = linPosHP[i][0]
            y = linPosHP[i][1]
            z = linPosHP[i][2]

            # update the position with respect to the
            # previously computed positions
            #self.head.x += x
            #self.head.y += y
            #self.head.z += z

        # Update the position

        # perform filtering on a per axis basis.
        # A = np.matrix([1])
        # H = np.matrix([1])
        # B = np.matrix([0])
        # Q = np.matrix([0.00001])
        # R = np.matrix([0.1])
        # xhat = np.matrix([3])
        # P    = np.matrix([1])

        # filter_x = KalmanFilterLinear(A,B,H,xhat,P,Q,R)
        # filter_y = KalmanFilterLinear(A,B,H,xhat,P,Q,R)
        # filter_z = KalmanFilterLinear(A,B,H,xhat,P,Q,R)

        # # Record the smooth'd values.
        # a_X = []
        # a_Y = []
        # a_Z = []

        # for i in range(0,len(acc)):
        #     measured_x = acc[i][0]    
        #     a_X.append(filter_x.GetCurrentState()[0,0])
        #     filter_x.Step(np.matrix([0]),np.matrix([measured_x]))

        #     measured_y = acc[i][1]    
        #     a_Y.append(filter_y.GetCurrentState()[0,0])
        #     filter_y.Step(np.matrix([0]),np.matrix([measured_y]))

        #     measured_z = acc[i][2]    
        #     a_Z.append(filter_z.GetCurrentState()[0,0])
        #     filter_z.Step(np.matrix([0]),np.matrix([measured_z]))

        t = 0.1
        for i in range(0,len(acc)):
            # a_x = a_X[0]
            # a_y = a_Y[1]
            # a_z = a_Z[2] - 1 # subtract 1 G from the up direction.
            
            a_x = acc[i][0]
            a_y = acc[i][1]
            a_z = acc[i][2] - 1

            x = (a_x*t*t);
            y = (a_y*t*t);
            z = (a_z*t*t);

            if x > 0.01 or x < 0:
                self.head.x = self.head.x + 10*(a_x*t*t);
            if y > 0.01 or y < 0:
                self.head.y = self.head.y + 10*(a_y*t*t);
            if z > 0.01 or z < 0:
                self.head.z = self.head.z + 10*(a_z*t*t);

        # original velocity vectors
        o_ux = rotation_matrices[0][0,0]
        o_vx = rotation_matrices[0][1,0]
        o_wx = rotation_matrices[0][2,0]

        o_uy = rotation_matrices[0][0,1]
        o_vy = rotation_matrices[0][1,1]
        o_wy = rotation_matrices[0][2,1]

        o_uz = rotation_matrices[0][0,2]
        o_vz = rotation_matrices[0][1,2]
        o_wz = rotation_matrices[0][2,2]

        # final velocity vectors
        f_ux = rotation_matrices[N-1][0,0]
        f_vx = rotation_matrices[N-1][1,0]
        f_wx = rotation_matrices[N-1][2,0]

        f_uy = rotation_matrices[N-1][0,1]
        f_vy = rotation_matrices[N-1][1,1]
        f_wy = rotation_matrices[N-1][2,1]

        f_uz = rotation_matrices[N-1][0,2]
        f_vz = rotation_matrices[N-1][1,2]
        f_wz = rotation_matrices[N-1][2,2]

        # time in microseconds between the measurements
        t = np.sum(del_t)

        # compute the angles
        # inv cos of the dot product.
        #self.head.xangle = np.dot([o_ux, o_vx, o_wx], [f_ux, f_vx, f_wx])
        #self.head.xangle = np.arccos(self.head.xangle)

        #self.head.yangle = np.dot([o_uy, o_vy, o_wy], [f_uy, f_vy, f_wy])
        #self.head.yangle = np.arccos(self.head.yangle)

        #self.head.zangle = np.dot([o_uz, o_vz, o_wz], [f_uz, f_vz, f_wz])
        #self.head.zangle = np.arccos(self.head.zangle)

        x, y, z = 0, 0, 0
        for i in range(0,N):
            x, y, z += (self.euler_from_matrix(rotation_matrices[i])/N)
            # maybe do a weighted avg instead
        
        self.head.xangle += x * 2
        self.head.yangle += y * 2
        self.head.zangle += z * 2
        #self.head.xangle, self.head.yangle, self.head.zangle = self.euler_from_matrix(rotation_matrices[N-1])
        self.head.rot_matrix = rotation_matrices[N-1]

    def update_head(self):
        """

        """

        data_window = {"acc" : [], "gyr" : [], "time" : []}
        init_window = False      
        S = 0  # data window size
        while True:
            if not init_window:
                if len(Controller.imu_measurements["acc"]) > 20:
                    data = copy.copy(Controller.imu_measurements)
                    data_window["acc"] = data["acc"]
                    data_window["gyr"] = data["gyr"]
                    data_window["time"] = data["time"]
                    S = len(data_window["acc"]);
                    init_window = True

            if init_window and len(Controller.imu_measurements["acc"]) > 10:
                data = copy.copy(Controller.imu_measurements)
                # number of data points.
                n = len(data["acc"])

                # shift the latter data points foward
                # and add the next n measurements to the end of the
                # data_window.
                data_window["acc"][0:S-n] = data_window["acc"][(S-n):S]
                data_window["acc"][(S-n):S] = data["acc"]
                
                data_window["gyr"][0:S-n] = data_window["gyr"][(S-n):S]
                data_window["gyr"][(S-n):S] = data["gyr"]

                data_window["time"][0:S-n] = data_window["time"][(S-n):S]
                data_window["time"][(S-n):S] = data["time"]  

                acc = data_window["acc"][1:n]
                gyr = data_window["gyr"][1:n]
                del_t = list()

                for i in range(1,n):
                    del_t.append(\
                        data_window["time"][i]-data_window["time"][i-1])

                # NOTE: use locks
                Controller.imu_measurements = \
                    {"acc" : [], "gyr" : [], "time" : []}
                self.process_data(acc, gyr, del_t)


if __name__ == "__main__":
    h = Head()
    c = Controller(h)

    while True:
        time.sleep(1)
        print(h)
