from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import numpy
import math
from math import sin,cos,tan,radians
import sys

import head
import shape

class View:
    def __init__(self, head, shape, dots):
        # GLUT initialization in program global, so initialize it on
        # the process level. It might be
        glutInit(sys.argv)

        self.head = head
        self.shape = shape
        self.dots = dots
        self.fps = 60
        self.width = 0
        self.height = 0
        
        self.points = []

        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(256,224)
        self.window = glutCreateWindow(b"GL")

    def TexFromPNG(self, filename=b'', data=None):
        if data is None:
            img = Image.open(filename)
            img_data = numpy.array(list(img.getdata()), numpy.uint8)
        else:
            img_data = data

        texture = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glBindTexture(GL_TEXTURE_2D, texture)

        # Texture parameters are part of the texture object, so you need to
        # specify them only once for a given texture object.
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0,
                GL_RGB, GL_UNSIGNED_BYTE, img_data)

        return texture

    def run(self):

        self.Tex = self.TexFromPNG(b"image.png")

        glutReshapeFunc(self.on_reshape)
        glutDisplayFunc(self.on_display)

        self.on_timer()
        glutMainLoop()

    def on_timer(self, value=0):
        # TODO: track actual time, since GLUT does not guarantee actual time
        #       passed
        glutPostRedisplay();
        glutTimerFunc(1000//self.fps, self.on_timer, value + 1)

    def on_reshape(self, width, height):
        self.width = width
        self.height = height
        glutPostRedisplay();

    def on_display(self):
        try:
            self.draw()
        except Exception as e:
            print(e)
            sys.exit(1)

    def draw(self):
        glViewport(0, 0, self.width//2, self.height)

        glClearDepth(1) # just for completeness
        glClearColor(0,0,0,0)
        glClear(GL_COLOR_BUFFER_BIT)

        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

        self.draw_camera(-1)
        glViewport(self.width//2, 0, self.width//2, self.height)
        self.draw_camera(1)

        # This implies a glFinish, which includes a glFlush
        glutSwapBuffers()

    def draw_camera(self, offset):
        ''' Draw the left or right eye camera. The eye is determined by the
        offset, 1 = right, -1 = left.
        '''

        screen_ratio = 1080/1920
        distance = math.sqrt(
                    (self.head.x - self.shape.x) ** 2 +
                    (self.head.y - self.shape.y) ** 2 +
                    (self.head.z - self.shape.z) ** 2
                )

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()

        glScalef(0.5, 1, 1)

        #turn everything into centimeters..
        glScalef(screen_ratio, 1, 1)

        # cut of from z=-1 to z=-1000
        gluPerspective(self.head.fov, screen_ratio, 0.02, 1000)
        gluLookAt(
                #                @ object
                #    +--------+ /
                #    |   ^up  |/
                #    |eye|    |
                #    |        |
                #    +--------+

                # eye location
                (self.head.eye_distance * offset) + self.head.x,
                self.head.y,
                self.head.z + 1,

                # Key controller mode
                cos(radians(self.head.xangle)) * distance,
                cos(radians(self.head.yangle)) * distance,
                -1*cos(radians(self.head.zangle)) * distance,

                # IMU mode 
                #math.cos(self.head.zangle)*math.cos(self.head.yangle),
                #math.sin(self.head.zangle)*math.cos(self.head.yangle),
                #math.sin(self.head.yangle),

                # the up vector in the final view.
                0, 1, 0
                )

        self.draw_view()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()


    def draw_view(self):
        ''' Draw the view from the camera, with a specified offset from the center
        '''

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        # rotate shape
        glRotatef(self.shape.zangle, 0, 0, 1)
        glRotatef(self.shape.yangle, 0, 1, 0)
        glRotatef(self.shape.xangle, 1, 0, 0)

        #if self.shape is not None:
            #self.draw_shape()
        if self.dots is not None:
            self.draw_lines()

        glPopMatrix()


    def draw_shape(self):
        glEnable(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, self.Tex)

        glBegin(GL_QUADS)

        glNormal3f(0.0, 0.0, 1.0)

        #print(self.shape)

        glTexCoord2f(0.0, 0.0)
        glVertex3f(-self.shape.width, -self.shape.height, 0.0)

        glTexCoord2f(1.0, 0.0)
        glVertex3f( self.shape.width, -self.shape.height, 0.0)

        glTexCoord2f(1.0, 1.0)
        glVertex3f( self.shape.width, self.shape.height, 0.0)

        glTexCoord2f(0.0, 1.0)
        glVertex3f(-self.shape.width, self.shape.height, 0.0)

        glEnd();

    def draw_lines(self):
        glLineWidth(3);
        
        # clear out points when neccassary 
        if (self.dots.is_clean_slate()):
            self.points = []

	# decide if two new points are useful
<<<<<<< HEAD
        point1, point2 = self.dots.getLastTwo()
        #print(point1, point2)
=======
        point1, point2 = self.dots.get_last_two()
>>>>>>> e3f0241130f3c2c2ba936a1ee6e8c6e172639a24
        if point1 and point2 and not \
            ((point1[0] > 62000 or point1[1] > 62000 or point1[2] > 62000) or \
            (point2[0] > 62000 or point2[1] > 62000 or point2[2] > 62000)):
            # magic numbers (2 * depthsense number code for bad data)
           

            
            # starting direction = (0,0,1) * distance = (0,0, distance) = starting origin
            # starting angles produce vector (0,0,1) in both imu and keyboard
            # goal: find new origin 

            # | ------ distance ------ |
            #
            # head --- \
            #           \ --- \
            #                  \ --- obj
            # (that was suppose to be a diagonal line, but think of it as any line)
            # we know that direction based off of imu angles
            # 
            # normalize this direction vector * distance = new origin
            # 

            # measure distance to obj from camera/persons head/imu location w.e you wanna call it
            distance = math.sqrt(
                (self.head.x - point2[0]/100) ** 2 +
                (self.head.y - point2[1]/100) ** 2 +
                (self.head.z - point2[2]/100) ** 2
            )

            # using mouse/keyboard angles (i left distance in there but it should be removed)
            sx, sy, sz = cos(radians(self.head.xangle)) * distance, \
                    cos(radians(self.head.yangle)) * distance, \
                    -1*cos(radians(self.head.zangle)) * distance
            
            # using imu angles
            #sx, sy, sz = math.cos(self.head.zangle)*math.cos(self.head.yangle), \
            #    math.sin(self.head.zangle)*math.cos(self.head.yangle), \
            #    math.sin(self.head.yangle),
                
            # normalize the vecotr (will rescale with the distance we need to cover)
            ns = math.sqrt(sx*sx + sy*sy + sz*sz)
            #print(sx/ns, sy/ns, sz/ns, distance)
            # store points with updated location (deals with the redrawing problem later)
            self.points.append((self.head.x + point1[0]/100 - sx/ns*distance, self.head.y + point1[1]/100 - sy/ns*distance, point1[2]/100))
            self.points.append((self.head.x + point2[0]/100 - sx/ns*distance, self.head.y + point2[1]/100 - sy/ns*distance, point2[2]/100))


        # bail if no points
        if len(self.points) < 2:
            return

        # redraw all points (TODO: find way of just appending points instead of redrawing everything)
        point0 = self.points[0]
        glBegin(GL_LINES)
        for point in self.points[1:]:

            # pick colour based on depth
            red = (1 - ((point0[2] + point[2])%50)/50)/4 # doesnt matter what we do here
            blue = 1 - (((point0[2] + point[2])%50)/50) # doesnt matter what we do here
            green = (1 -  ((point0[2] + point[2])%50)/50)/4 # doesnt matter what we do here
            glColor3f(red,green,blue)

            glVertex3f(point0[0] ,
                   point0[1],
                   point0[2]*-1)
            glVertex3f(point[0],
                   point[1],
                   point[2]*-1)

            point0 = point

        glEnd()

    def draw_circles(self, radius):
        # ignore this func, i wanted to represent hands as circles but .. yea
        point1, point2 = self.dots.get_last_two()
        if point1 and point2 and point1 != 64002 and point2 != 64002: # magic numbers (2 * depthsense number code for bad data)
            x,y = point2[0]/100,point2[1]/100
            glColor3f(1,0,0)
            # Todo translate 2D circle to the z = -1 plane (i believe its drawn behind the camera now)
            glBegin(GL_LINE_LOOP);
            for i in range(0,360):
                glVertex2f(x + cos(radians(i)*radius/100), y + sin(radians(i)*radius/100))
            glEnd()



if __name__ == "__main__":
    thing = View()
    thing.run()
