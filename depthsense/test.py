import DepthSense as ds
import numpy as np
from SimpleCV import *
c = 0
ds.initDepthSense()
while True:
    depth = ds.getDepthMap()

    print "START"
    print depth[100][100]
    np.clip(depth, 0, 2**10 - 1, depth)
    print depth[100][100]
    depth >>=2
    print depth[100][100]
    depth = depth.astype(np.uint8).transpose()
    print depth[100][100]
    print "END"
    iD = Image(depth)
    
    #iD = Image(depth.transpose())
    image = ds.getColourMap()
    image = image[:,:,::-1]
    iS = Image(image.transpose([1,0,2]))
    iS.sideBySide(iD).show()
    #iD.show()
    #iS.show()
    c+=1 
    if c > 10000:
        ds.killDepthSense()
        break
    
