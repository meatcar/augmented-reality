#!/bin/python2
from ds325 import DS325
from SimpleCV import *
#c = 0
depthsense = DS325()
while True:
    #iB = depthsense.getBlob(100,100, 5, 5)

    iD = depthsense.getDepth() 
    iE = depthsense.getEdges("edge")

    iDH = depthsense.getDepthFull()
    iEH = depthsense.getEdgesFull("edge")

    #iDH.sideBySide(iEH).show()
    iD.sideBySide(iE).show()
