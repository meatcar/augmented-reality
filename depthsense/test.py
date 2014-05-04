#!/bin/python2
from ds325 import DS325
from SimpleCV import *
#c = 0
depthsense = DS325()
while True:
    #iB = depthsense.getBlob(100,100, 5, 5)

    #iC = depthsense.getImage()
    #iD = depthsense.getDepth() 
    #iE = depthsense.getEdges("edgh", 1)

    #iDH = depthsense.getDepthFull()
    #iEH = depthsense.getEdgesFull("edgh", 1)

    iH = depthsense.getDepthColoured()

    iH.show()
    #iDH.sideBySide(iEH).show()
    #iD.sideBySide(iE).show()
    #iC.sideBySide(iE).show()

