#!/bin/python2

import DepthSense as ds
import numpy as np
import copy as copy
from SimpleCV import *
import sys
from time import sleep

ds.initDepthSense()
#disp = Display(flags = pg.FULLSCREEN)
disp = Display()
points = []
squares = []

# Main loop closes only on keyboard kill signal 
while True: 
 
    # Get depth and colour images from the kinect
    image = ds.getColourMap()
    image = image[:,:,::-1]
    img = Image(image.transpose([1,0,2]))
 
    depth = ds.getDepthMap()
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>=2
    depth = depth.astype(np.uint8).transpose()
    depth = Image(depth)
    depth = depth.invert()
 
    #vertex = ds.getVertices()
    #vertex = vertex.transpose([1,0,2])

    #dblobs = depth.findBlobs(minsize=2000, maxsize=14000)
    dblobs = depth.findBlobs(minsize=2000)
 
    box_center = None
    box = None
    box_point = None
    z_val = 0
    box_area = 0
    counter = 0
    if not dblobs:
        if len(points) > 2:
            depth.dl().lines(points, Color.BLUE, width=2)
        #depth.show()
        depth.save(disp)
        continue

    # assume biggest blob is hand
    b = dblobs[-1]
    # filter out region of depth above given colour distance (focuses our interest)
    if ((depth[b.centroid()] < (200,200,200)) \
        and b.rectangleDistance() > 0.15):
        #print depth[b.centroid()], b.area(), b.rectangleDistance()


        bb = b.boundingBox()
        box_center = b.centroid()
        hand = b.contour()
        #sorted_hand = copy(hand)
        #sorted_hand.sort(key=lambda x: x[1])
        box_point = [(top_x, top_y) for (top_x, top_y) in hand if top_y == min([y for (x,y) in hand])][0]
        #box_point = sorted_hand[0]

        val = sum([(abs(p[0] - box_point[0])) for p in hand if (abs(p[1] - box_point[1]) < 8)])
        if val > 150:
            #print val
            box_center = None
            depth.drawRectangle(bb[0], bb[1], bb[2], bb[3], color=Color.VIOLET)
            continue

        depth.dl().circle(box_point, 20, Color.RED)
        depth.dl().polygon(hand, filled=True, color=Color.YELLOW)
        depth.drawRectangle(bb[0], bb[1], bb[2], bb[3], color=Color.GREEN)

 
    # search within the colour image if no hand found
    if box_center == None:
        bigb = dblobs[-1]
        bigarea = bigb.area()
        if bigarea < 320*240:
            bigbb = bigb.boundingBox()
            cropped = img.crop(bigbb[0]/2, bigbb[1]/2, bigbb[2]*2, bigbb[3]*2)
            #cropped.save(disp)
            hands = cropped.findSkintoneBlobs()
            if hands:
                hand = hands[-1]
                hand = [(px + bigbb[0]/2, py + bigbb[1]/2) for (px, py) in hand.contour()]
                col_point = [(tpx, tpy) for (tpx, tpy) in hand if tpy == min([y for (x,y) in hand])][0]
                depth.dl().polygon(hand, color=Color.LEGO_BLUE)
                depth.dl().circle(col_point, 20, Color.RED)

            depth.dl().polygon(bigb.contour(), color=Color.HOTPINK)

    # append new point to the point array
    if (len(points) > 0) and (box_center):
        x_delta = abs(box_point[0] - points[-1][0])
        y_delta = abs(box_point[1] - points[-1][1])
        if (x_delta < 100 and y_delta < 100):
            points.append(box_point)
        else:
            # point found faraway from previous point, restart array
            points = []
            points.append(box_point)
    
    # first point in the scene
    elif (box_center):
        points.append(box_point)
 
 
    # draw lines
    if len(points) > 2:
        depth.dl().lines(points, Color.BLUE, width=2)
 
    # draw box
    #if len(squares) == 2:
    #    depth.dl().rectangle2pts(squares[0], squares[1], Color.RED, width=3, filled=False,)
 
    # draw scene
    depth.save(disp)
