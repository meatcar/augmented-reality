from threading import Thread
import depth
def dummy():
    depth.initDepthMap()
    return

t = Thread(target = dummy)
t.start()
print "still alive"
print depth.getDepthMap()
print "doing goooood"
