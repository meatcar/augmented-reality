import DepthSense as ds
import numpy as np
from SimpleCV import Image

class DS325:
    ''' DepthSense camera class for simple cv '''

    def __init__(self, dim=[320,240]):
        # TODO: Pass in dim to init (currently defaults to 640, 480 for camera)
        # TODO: Allow for enabling camera/depth/accel independantly
        ''' The maps returned by the ds mod are not transposed, the maps
        used ''' 
        ds.initDepthSense()

    def getDepth(self):
        ''' Return a simple cv compatiable 8bit depth image '''

        depth = ds.getDepthMap()
        np.clip(depth, 0, 2**10 - 1, depth)
        depth >>=2
        depth = depth.astype(np.uint8)
        iD = Image(depth.transpose())
        return iD.invert()

    def getDepthFull(self):
        ''' Return the pure 16bit depth map as a numpy array '''

        return ds.getDepthMap()

    def getVertex(self):
        ''' Return a vertex map for points in the depth map as a numpy array'''

        return ds.getVertices()

    def getImage(self):
        ''' Return a simple cv compatiable 8bit colour image ''' 

        image = ds.getColourMap()
        image = image[:,:,::-1]
        return Image(image.transpose([1,0,2]))

    def getAcceleration(self):
        ''' Return the current acceleration of the device (x,y,z) measured in 
        g force as a numpy array '''

        return ds.getAcceleration()

    def getUV(self):
        ''' Return a uv map, the map represents a conversion from depth 
        indicies to scaled colour indicies from 0 - 1 '''

        return ds.getUVMap()

    def getSync(self):
        ''' Return a simplecv compatiable synced map with dimensions of the 
        depth map and colours from the colour map. Indexes here match indexes 
        in the vertex map '''

        sync = ds.getSyncMap()
        sync = sync[:,:,::-1]
        return Image(sync.transpose([1,0,2]))

    def getSyncFull(self):
        ''' Return a colour synced depth map, like above indicies here work on
        both the depth map and vertex map '''

        return ds.getSyncMap()

