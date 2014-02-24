"""


"""

# misc imports.
import sys
import time
import copy
import math
from threading import Thread

# imports for processing IMU data.
from MadgwickAHRS import MadgwickAHRS

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

        samplePeriod = 1/256
        self.ahrs = MadgwickAHRS(samplePeriod)
        #t = Thread(target=self.update_head)
        #t.daemon = True
        #t.start()
        self.x = 0
        self.y = 0
        self.z = 0
        self.update_head()

    def update_head(self):
        """

        """
        while True:
            data = copy.copy(Controller.imu_measurements)
            if (len(data[0]) + len(data[1]) + len(data[2]) == 9):
                self.ahrs.update(
                    data[0][0], data[0][1], data[0][2],
                    data[1][0], data[1][1], data[1][2],
                    data[2][0], data[2][1], data[2][2]
                )
        
                x, y, z = self.ahrs.getEulerAngles()
                self.x += x
                self.y += y
                self.z += z
                if self.prev != data[3]:
                    print ("")
                    print(self.x % 6.28, self.y % 6.28, self.z % 2*3.14)
                    #print (self.ahrs.quatern2rotMat())
                    print (data)
                    print ("")
                    #print (data[3])
                self.prev = data[3]


c = Controller()
while True:
    pass
