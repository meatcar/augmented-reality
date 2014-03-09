from SimpleCV import *
import DepthSense as ds
ds.initDepthSense()
points = []
squares = []
while True:
    try:

        #img = k.getImage()
        depth = ds.getDepthMap()
        np.clip(depth, 0, 2**10 - 1, depth)
        depth >>=2
        depth = depth.astype(np.uint8).transpose()
        depth = Image(depth)
        depth.stretch(0,150)
        dark = depth
        dblobs = dark.findBlobs()
        if not dblobs:
            continue

        for b in dblobs:
            if ((sum(depth[b.centroid()]) > 150) and (sum(depth[b.centroid()]) < 600) and (b.area() > 50000)):
            #if b.area() > 50000:
                b.draw(Color.RED, width=1)
                print b.area(), depth[b.centroid()], len(dblobs)
        dark.show()
    except KeyboardInterrupt:
        break
