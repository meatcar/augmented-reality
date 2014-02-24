import math
import numpy as np

class MadgwickAHRS:


    def __init__(self, period, beta=0.1):
        self.period = period
        self.beta = beta
        self.Quaternion = [1.0, 0.0, 0.0, 0.0]


    def update(self, gx, gy, gz,   # gyroscope 
                     ax, ay, az,   # accelerometer
                     mx, my, mz):  # magnetometer
            
        # the crew 
        q1 = self.Quaternion[0]; q2 = self.Quaternion[1]; 
        q3 = self.Quaternion[2]; q4 = self.Quaternion[3];

        # Auxiliary variables to avoid repeated arithmetic
        _2q1 = 2.0 * q1
        _2q2 = 2.0 * q2
        _2q3 = 2.0 * q3
        _2q4 = 2.0 * q4
        _2q1q3 = 2.0 * q1 * q3
        _2q3q4 = 2.0 * q3 * q4
        q1q1 = q1 * q1
        q1q2 = q1 * q2
        q1q3 = q1 * q3
        q1q4 = q1 * q4
        q2q2 = q2 * q2
        q2q3 = q2 * q3
        q2q4 = q2 * q4
        q3q3 = q3 * q3
        q3q4 = q3 * q4
        q4q4 = q4 * q4

        # normalize accelermoter
        norm = math.sqrt(ax * ax + ay * ay + az * az)
        if (norm == 0.0): 
            return

        norm = 1.0/norm
        ax *= norm
        ay *= norm
        az *= norm

        # normalize magnetometer
        norm = math.sqrt(mx * mx + my * my + mz * mz)
        if (norm == 0.0): 
            return

        norm = 1.0/norm
        mx *= norm
        my *= norm
        mz *= norm

        # earth mag field direction
        _2q1mx = 2.0 * q1 * mx
        _2q1my = 2.0 * q1 * my
        _2q1mz = 2.0 * q1 * mz
        _2q2mx = 2.0 * q2 * mx

        hx = mx * q1q1 - _2q1my * q4 + _2q1mz * q3 + mx * q2q2 + _2q2 * my * q3 \
                + _2q2 * mz * q4 - mx * q3q3 - mx * q4q4
        hy = _2q1mx * q4 + my * q1q1 - _2q1mz * q2 + _2q2mx * q3 - my * q2q2 + \
                my * q3q3 + _2q3 * mz * q4 - my * q4q4

        _2bx = math.sqrt(hx * hx + hy * hy)
        _2bz = -_2q1mx * q3 + _2q1my * q2 + mz * q1q1 + _2q2mx * q4 - mz * q2q2 \
                + _2q3 * my * q4 - mz * q3q3 + mz * q4q4

        _4bx = 2.0 * _2bx
        _4bz = 2.0 * _2bz

        #  Gradient desceeeenntt
        s1 = -_2q3 * (2.0 * q2q4 - _2q1q3 - ax) + _2q2 * (2.0 * q1q2 + _2q3q4 - \
                ay) - _2bz * q3 * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - \
                q1q3) - mx) + (-_2bx * q4 + _2bz * q2) * (_2bx * (q2q3 - q1q4) \
                + _2bz * (q1q2 + q3q4) - my) + _2bx * q3 * (_2bx * (q1q3 + q2q4) \
                + _2bz * (0.5 - q2q2 - q3q3) - mz)
        s2 = _2q4 * (2.0 * q2q4 - _2q1q3 - ax) + _2q1 * (2.0 * q1q2 + _2q3q4 - \
                ay) - 4.0 * q2 * (1 - 2.0 * q2q2 - 2.0 * q3q3 - az) + _2bz * q4 \
                * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + \
                (_2bx * q3 + _2bz * q1) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 \
                + q3q4) - my) + (_2bx * q4 - _4bz * q2) * (_2bx * (q1q3 + q2q4) \
                + _2bz * (0.5 - q2q2 - q3q3) - mz)
        s3 = -_2q1 * (2.0 * q2q4 - _2q1q3 - ax) + _2q4 * (2.0 * q1q2 + _2q3q4 - \
                ay) - 4.0 * q3 * (1 - 2.0 * q2q2 - 2.0 * q3q3 - az) + (-_4bx * \
                q3 - _2bz * q1) * (_2bx * (0.5 - q3q3 - q4q4) + _2bz * (q2q4 - \
                q1q3) - mx) + (_2bx * q2 + _2bz * q4) * (_2bx * (q2q3 - q1q4) + \
                _2bz * (q1q2 + q3q4) - my) + (_2bx * q1 - _4bz * q3) * (_2bx * \
                (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz)
        s4 = _2q2 * (2.0 * q2q4 - _2q1q3 - ax) + _2q3 * (2.0 * q1q2 + _2q3q4 - \
                ay) + (-_4bx * q4 + _2bz * q2) * (_2bx * (0.5 - q3q3 - q4q4) + \
                _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q1 + _2bz * q3) * (_2bx * \
                (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + _2bx * q2 * (_2bx * \
                (q1q3 + q2q4) + _2bz * (0.5 - q2q2 - q3q3) - mz)

        norm = 1.0 / math.sqrt(s1 * s1 + s2 * s2 + s3 * s3 + s4 * s4)   # normalise step magnitude
        s1 *= norm;
        s2 *= norm;
        s3 *= norm;
        s4 *= norm;

        # Compute rate of change of quaternion
        qDot1 = 0.5 * (-q2 * gx - q3 * gy - q4 * gz)    - self.beta * s1;
        qDot2 = 0.5 * (q1 * gx + q3 * gz - q4 * gy)     - self.beta * s2;
        qDot3 = 0.5 * (q1 * gy - q2 * gz + q4 * gx)     - self.beta * s3;
        qDot4 = 0.5 * (q1 * gz + q2 * gy - q3 * gx)     - self.beta * s4;
        
        # Integrate to yield quaternion
        q1 += qDot1 * self.period;
        q2 += qDot2 * self.period;
        q3 += qDot3 * self.period;
        q4 += qDot4 * self.period;
        
        norm = 1.0 / math.sqrt(q1 * q1 + q2 * q2 + q3 * q3 + q4 * q4)   # normalise quaternion
        self.Quaternion[0] = q1 * norm;
        self.Quaternion[1] = q2 * norm;
        self.Quaternion[2] = q3 * norm;
        self.Quaternion[3] = q4 * norm;

        return

    def getEulerAngles(self):
        qw = self.Quaternion[0]; qx = self.Quaternion[1]; 
        qy = self.Quaternion[2]; qz = self.Quaternion[3];
        
        w2 = qw*qw
        x2 = qx*qx
        y2 = qy*qy
        z2 = qz*qz
        unitLength = w2 + x2 + y2 + z2      # Normalised == 1, otherwise correction divisor.
        abcd = qw*qx + qy*qz
        eps = 1e-7;    # TODO: pick from your math lib instead of hardcoding.
        pi = 3.14159265358979323846;    # TODO: pick from your math lib instead of hardcoding.
        if (abcd > (0.5-eps)*unitLength):
            yaw = 2.0 * math.atan2(qy, qw)
            pitch = pi
            roll = 0.0

        elif (abcd < (-0.5+eps)*unitLength):
            yaw = -2.0 * math.atan2(qy, qw)
            pitch = -pi
            roll = 0.0
        else:
            adbc = qw*qz - qx*qy
            acbd = qw*qy - qx*qz
            yaw = math.atan2(2.0*adbc, 1.0 - 2.0*(z2+x2))
            pitch = math.asin(2.0*abcd/unitLength)
            roll = math.atan2(2.0*acbd, 1.0 - 2.0*(y2+x2));


        return yaw, pitch, roll
        
    def quatern2rotMat(self):
        q = self.Quaternion
        R = np.zeros(shape=(3,3))

        R[0,0] = 2 * q[0]**2 - 1 + 2 * q[1]**2
        R[0,1] = 2 * (q[1] * q[2] + q[0] * q[3])
        R[0,2] = 2 * (q[1] * q[3] - q[0] * q[2])

        R[1,0] = 2 * (q[1] * q[2] - q[0] * q[3])
        R[1,1] = 2 * q[0]**2 - 1 + 2 * q[2]**2
        R[1,2] = 2 * (q[2] * q[3] + q[0] * q[1])

        R[2,0] = 2 * (q[1] * q[3] + q[0] * q[2])
        R[2,1] = 2 * (q[2] * q[3] - q[0] * q[1])
        R[2,2] = 2 * q[0]**2 - 1 + 2 * q[3]**2

        return R
