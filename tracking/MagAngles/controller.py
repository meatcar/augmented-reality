"""


"""

# misc imports.
import sys
import time
import copy
import math
from threading import Thread

# imports for processing IMU data.
import numpy as np

# imports for handling IMU.
from ctypes import *
from Phidgets.Phidget import Phidget
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import SpatialDataEventArgs, AttachEventArgs
from Phidgets.Events.Events import DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Spatial import Spatial, SpatialEventData, TimeSpan


class Controller(object):
    """

    """
    # stores acceleration gyroscope, magnetic, time.
    imu_measurements = [[], [], [], 0]

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

    class IMU_Handlers(object):
        """

        """

        def on_data(self, e):
            """

            """
            source = e.device
            for index, spatialData in enumerate(e.spatialData):
            
                if  (len(spatialData.Acceleration) == 3) and (len(spatialData.AngularRate)  == 3) \
                        and (len(spatialData.MagneticField) == 3):

                    acc = [spatialData.Acceleration[0], spatialData.Acceleration[1], spatialData.Acceleration[2]]
                    gyr = [spatialData.AngularRate[0], spatialData.AngularRate[1], spatialData.AngularRate[2]]
                    mag = [spatialData.MagneticField[0], spatialData.MagneticField[1], spatialData.MagneticField[2]]

                    Controller.imu_measurements[0] = gyr
                    Controller.imu_measurements[1] = acc
                    Controller.imu_measurements[2] = mag
                    Controller.imu_measurements[3] = spatialData.Timestamp.seconds

                    break;

        def on_attach(self, e):
            """

            """

            return

        def on_detach(self, e):
            """

            """

            return

        def on_error(self, e):
            """

            """

            try:
                source = e.device
                print(("Spatial %i: Phidget Error %i: %s" % \
                    (source.getSerialNum(), e.eCode, e.description)))
            except PhidgetException as e:
                print(("Phidget Exception %i: %s" % (e.code, e.details)))

    def __init__(self):
        """

        """

        # update from the IMU.
        self.spatial = Spatial()
        imu_handlers = Controller.IMU_Handlers()
        self.prev = 0

        # attach the event handlers.
        try:
            self.spatial.setOnAttachHandler(imu_handlers.on_attach)
            self.spatial.setOnDetachHandler(imu_handlers.on_detach)
            self.spatial.setOnErrorhandler(imu_handlers.on_error)
            self.spatial.setOnSpatialDataHandler(imu_handlers.on_data)

            self.spatial.openPhidget()
            self.spatial.waitForAttach(10000)
            self.spatial.setDataRate(4)

        except:
            print("Error connecting to IMU, I cannot handle this. " + \
            "I will just go die now!")
            exit(1)

        #t = Thread(target=self.update_head)
        #t.daemon = True
        #t.start()
        self.x = 0
        self.y = 0
        self.z = 0

        data = copy.copy(Controller.imu_measurements)
        while (len(data[2]) != 3):
            data = copy.copy(Controller.imu_measurements)


        print ("here")
        mag_v = np.array(data[2])
        norm = np.linalg.norm(mag_v)
        mag_v = mag_v/norm
        x = mag_v[0]
        y = mag_v[1]
        z = mag_v[2]

        # intial reference frame
        self.state  = [x, y, z]
        self.update_head()

    def update_head(self):
        """

        """
        while True:
            data = copy.copy(Controller.imu_measurements)
            if (len(data[0]) + len(data[1]) + len(data[2]) == 9):
                #self.ahrs.update(
                #    data[0][0], data[0][1], data[0][2],
                #    data[1][0], data[1][1], data[1][2],
                #    data[2][0], data[2][1], data[2][2]
                #)
        
                
                mag_v = np.array(data[2])
                norm = np.linalg.norm(mag_v)
                mag_v = mag_v/norm

                x = mag_v[0]
                y = mag_v[1]
                z = mag_v[2]

                if self.prev != data[3]:
                    print ("")
                    print([x, y, z])
                    print(self.state)
                    print(math.acos(np.dot(self.state, [x,y,z]))) 
                    print(self.state[0] - x, self.state[1] - y, self.state[2] - z)
                    #print (self.ahrs.quatern2rotMat())
                    #print (data)
                    print ("")
                    #print (data[3])

                self.x = x
                self.y = y
                self.z = z

                self.prev = data[3]


c = Controller()
while True:
    pass
