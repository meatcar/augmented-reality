from SimpleCV import *
k = Kinect()
#size = (k.getImage().size())
#disp = Display(size)
disp = Display(flags = pg.FULLSCREEN)
fs1 = []
points = []
squares = []
blob_mask = None

while disp.isNotDone():
    try:
        depth = k.getDepth()
        dark = depth - depth.colorDistance((80,80,80))
        dblobs = dark.findBlobs(minsize=1000)
        img = k.getImage().crop(0,25, 605, 455).scale(640,480)
        #img.dl().blit(img.crop(100, 25, 515, 455), (125,0))

        box_center = None
        box_point = None
        box = None
        box_area = 0
        counter = 0
        cropped = None
        for b in dblobs:
            if depth[b.centroid()] < (120,120,120):
                # save old info
                old_point = box_point
                old_center = box_center
                old_box = box

                # get info on new box
                box = b.minRect()
                bb = b.boundingBox()
                bb[0]-=20
                bb[3] = bb[3] - bb[3]/4
                box_center = b.centroid()
                cropped = img.crop(bb[0]-20, bb[1], bb[2], (bb[3] - bb[3]/5))
                blobs = cropped.findSkintoneBlobs()
                blob_mask = blobs[-1].blobImage()
                hand = blobs[-1].contour()
                hand_adj = []
                for p in hand:
                    hand_adj.append((p[0] + bb[0] - 20, p[1] + bb[1]))

                # get box with min y (i.e highest point)`
                top = (0,100000)
                for p in box:
                    if p[1] < top[1]:
                        top = p

                # define tip of box
                box_point = (top[0], top[1])
                # draw on hand for reference
                img.dl().circle(box_point, 20, Color.RED)
                b.drawMinRect(color=Color.GREEN, layer=img.dl())
                #b.draw(width=2, color=Color.BLUE, layer=img.dl())
                img.dl().polygon(b.contour(), color=Color.YELLOW)
                #img.dl().polygon(hand_adj, filled=True, color=Color.YELLOW)
                break

                # draw box btwn points if two hands are up
                #if counter == 2:
                #    if abs(old_point[0] - box_point[0]) > 100 and abs(box_point[1] - box_point[0]) > 100:
                #        squares = []
                #        top = box_point
                #        bottom = old_point
                #        squares.append(top)
                #        squares.append(bottom)
                #        break
                

        #print "count of matched obs: ", counter
        if (len(points) > 0) and (box_center):
            x_delta = abs(box_point[0] - points[-1][0])
            y_delta = abs(box_point[1] - points[-1][1])
            if (x_delta < 100 and y_delta < 100):
                points.append(box_point)
            else: 
                points = []
                points.append(box_point)
        elif (box_center):
            points.append(box_point)

    
    
        if len(points) > 2:
            img.dl().lines(points, Color.BLUE, width=4)
            #depth.dl().bezier(points, 3, Color.BLUE)

        #if len(squares) == 2:
        #    dark.dl().rectangle2pts(squares[0], squares[1], Color.RED, width=3, filled=False,)

        mask = Image(img.size())
        mask.addDrawingLayer(img.dl())
        mask = mask.applyLayers()
        mask.save(disp)

#        counter = 0
#        while blob_mask and counter < 5:
#            img = k.getImage().crop(0,25, 605, 455).scale(640,480)
#            blobs = img.findTemplateOnce(blob_mask, threshold=0.2, grayscale=False)
#            if not blobs:
#                counter+=1
#            else:
#                blobs.draw(color=Color.RED)
#            
#            img.save(disp)
#
        if disp.mouseLeft:
            disp.done = True
            pg.quit()


    except KeyboardInterrupt:
        break


