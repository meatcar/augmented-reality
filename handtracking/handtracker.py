from SimpleCV import *
disp = Display(flags = pg.FULLSCREEN)
k = Kinect()
points = []
squares = []
while disp.isNotDone():
    try:

        img = k.getImage()
        depth = k.getDepth()
        depth.stretch(0,150)
        dark = depth - depth.colorDistance((80,80,80))
        dblobs = dark.findBlobs(minsize=1000)
        
        box_center = None
        box = None
        box_point = None
        z_val = 0
        box_area = 0
        counter = 0
        for b in dblobs:
            if ((dark[b.centroid()] < (100,100,100)) and (dark[b.centroid()] > (40,40, 40)) ):
                box_x = b.minRectHeight()
                box_y = b.minRectWidth()
                new_box_area = box_x*box_y
                if new_box_area < 30000:
                    z_val = depth[b.centroid()][2]
                    old_point = box_point
                    old_box = box
                    old_center = box_center
                    box = b.minRect()
                    bb = b.boundingBox()
                    bb[0]-=50
                    bb[2]+=20
                    bb[3] = bb[3] - bb[3]/4
                    box_center = b.centroid()
                    box_area = new_box_area


                    cropped = img.crop(bb[0], bb[1], bb[2], bb[3])
                    blobs = cropped.findSkintoneBlobs()
                    if not blobs:
                        continue
                    blob_mask = blobs[-1].blobImage()
                    hand = blobs[-1].contour()
                    hand_adj = []
                    for p in hand:
                        hand_adj.append((p[0] + bb[0], p[1] + bb[1]))

                    box_point = [(top_x, top_y) for (top_x, top_y) in hand_adj if top_y == min([y for (x,y) in hand_adj])][0]
                    img.dl().circle(box_point, 20, Color.RED)
                    img.dl().polygon(hand_adj, filled=True, color=Color.YELLOW)
                    img.drawRectangle(bb[0], bb[1], bb[2], bb[3], color=Color.GREEN)
                    
                    counter+=1
                    if counter == 2:
                        if abs(old_point[0] - box_point[0]) > 100 and abs(box_point[1] - box_point[0]) > 100:
                            squares = []
                            top = box_point
                            bottom = old_point
                            squares.append(top)
                            squares.append(bottom)
                
    
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
            img.dl().lines(points, Color.BLUE, width=2)
            if z_val != 0:
                print z_val

        if len(squares) == 2:
            img.dl().rectangle2pts(squares[0], squares[1], Color.RED, width=3, filled=False,)


        img.save(disp)

        if disp.mouseLeft:
            disp.done = True
            pg.quit()


    except KeyboardInterrupt:
        break

