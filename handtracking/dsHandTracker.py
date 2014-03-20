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
    dblobs = depth.findBlobs(minsize=2000, maxsize=(320*240/2))
 
    box_center = None
    box = None
    box_point = None
    possible_hands = []
    z_val = 0
    box_area = 0
    counter = 0
    if not dblobs:
        if len(points) > 2:
            depth.dl().lines(points, Color.BLUE, width=2)
        #depth.show()
        depth.save(disp)
        continue
    for b in dblobs:
        # filter out region of depth above given colour distance (focuses our interest)
        if ((depth[b.centroid()] < (200,200,200)) \
                and (depth[b.centroid()] > (40,40, 40)) \
                and b.rectangleDistance() > 0.19):
            #print depth[b.centroid()], b.area(), b.rectangleDistance()

            old_point = box_point

            bb = b.boundingBox()
            hand = b.contour()
            #sorted_hand = copy(hand)
            #sorted_hand.sort(key=lambda x: x[1])
            box_point = [(top_x, top_y) for (top_x, top_y) in hand if top_y == min([y for (x,y) in hand])][0]
            #box_point = sorted_hand[0]

            val = sum([(abs(p[0] - box_point[0])) for p in hand if (abs(p[1] - box_point[1]) < 8)])
            if val > 150:
                #print val
                depth.drawRectangle(bb[0], bb[1], bb[2], bb[3], color=Color.ORANGE)
                #possible_hands.append(b)
                continue

            box_center = b.centroid()
            depth.dl().circle(box_point, 20, Color.RED)
            depth.dl().polygon(hand, filled=True, color=Color.YELLOW)
            depth.drawRectangle(bb[0], bb[1], bb[2], bb[3], color=Color.GREEN)

            # points that opengl can use
            #print vertex[(box_point[0], box_point[1])]
 
            # if two hands are found in the scene, record point information
            #counter+=1
            #if counter == 2:
            #    if abs(old_point[0] - box_point[0]) > 100 and abs(box_point[1] - box_point[0]) > 100:
            #        squares = []
            #        top = box_point
            #        bottom = old_point
            #        squares.append(top)
            #        squares.append(bottom)
            #        continue
 
 
    # search within the colour image if no hand found
    if box_center == None:
        possible_hands.append(dblobs[-1])
        bb = dblobs[-1].boundingBox()
        depth.drawRectangle(bb[0], bb[1], bb[2], bb[3], color=Color.YELLOW)
        for bigb in possible_hands:
            
            bigbb = bigb.boundingBox()
            x = bigbb[0]/2 + 20
            y = bigbb[1]/2 + 20
            
            if x < 0:
                x = 0
            elif x > 320:
                x = 320 - 20
            if y < 0:
                y = 0
            elif y > 240:
                y = 240 - 20
            
            cropped = img.crop(x, y, bigbb[2]*2, bigbb[3]*2)
            hands = cropped.findSkintoneBlobs(minsize=1000)
            if not hands:
                continue

            for hand in hands:
                print hand.rectangleDistance(), hand.area()
                if hand.rectangleDistance() < 0.1:
                    continue
                hand = [(px/2 + bigbb[0]/2, py/2 + bigbb[1]/2) for (px, py) in hand.contour()]
                col_point = [(tpx, tpy) for (tpx, tpy) in hand if tpy == min([y for (x,y) in hand])][0]
                depth.dl().polygon(hand, filled=True, color=Color.LEGO_BLUE)
                depth.dl().circle(col_point, 20, Color.RED)
                #depth.dl().polygon(bigb.contour(), color=Color.HOTPINK)

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
