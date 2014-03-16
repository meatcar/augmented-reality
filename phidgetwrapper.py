# imports for handling IMU.
from ctypes import *
from Phidgets.Phidget import Phidget
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import SpatialDataEventArgs, AttachEventArgs
from Phidgets.Events.Events import DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Spatial import Spatial, SpatialEventData, TimeSpan

class PhidgetWrapper(object):

    def __init__(self, data_callback):
        self.spatial = Spatial()
        self.callback = data_callback;

        # attach the event handlers.
        try:
            self.spatial.setOnAttachHandler(self.on_attach)
            self.spatial.setOnDetachHandler(self.on_detach)
            self.spatial.setOnErrorhandler(self.on_error)
            self.spatial.setOnSpatialDataHandler(self.on_data)

            self.spatial.openPhidget()
            self.spatial.waitForAttach(1000)
            self.spatial.setDataRate(4)
            self.spatial.setCompassCorrectionParameters(0.51236, 0.02523, 0.16216, 0.07254, 1.88718, 1.82735, 2.14068, -0.06096, -0.04644, -0.05897, 0.00783, -0.05211, 0.00870);

        except e:
            print("Error connecting to IMU, I cannot handle this. I will just go die now!", e)
            exit(1)

    def on_data(self, e):
        source = e.device
        for index, spatialData in enumerate(e.spatialData):
            if len(spatialData.Acceleration) > 0 and len(spatialData.AngularRate) > 0 and len(spatialData.MagneticField) > 0:
                acc = [spatialData.Acceleration[0], spatialData.Acceleration[1], spatialData.Acceleration[2]]
                gyr = [spatialData.AngularRate[0], spatialData.AngularRate[1], spatialData.AngularRate[2]]
                mag = [spatialData.MagneticField[0], spatialData.MagneticField[1], spatialData.MagneticField[2]]

                self.callback(acc, gyr, mag, spatialData.Timestamp.microSeconds)

    def on_attach(self, e):
        print('Phidget attached!')
        return

    def on_detach(self, e):
        print('Phidget detached!')
        return

    def on_error(self, e):
        try:
            source = e.device
            print(("Spatial %i: Phidget Error %i: %s" % \
                    (source.getSerialNum(), e.eCode, e.description)))
        except PhidgetException as e:
            print(("Phidget Exception %i: %s" % (e.code, e.details)))

def test_data(acc, agr, time):
    print('acc', acc, 'agr', agr, 'time', time)

if __name__ == "__main__":
    phidget = PhidgetWrapper(test_data)
    while True:
        continue

