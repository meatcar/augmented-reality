from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import numpy
from math import sin,cos,tan,radians,pi,sqrt,atan,atan2,acos,asin,degrees
import sys

import head
import shape
from constants import Mode

class View:
    def __init__(self, head, shape, dots, mode=Mode.IMU_MODE, line_width=3):
        # GLUT initialization in program global, so initialize it on
        # the process level. It might be
        glutInit(sys.argv)

        self.head = head
        self.shape = shape
        self.dots = dots
        self.fps = 60
        self.width = 0
        self.height = 0
        self.line_width = line_width
        self.mode = mode 
        self.points = []

        glutInitDisplayMode(GLUT_RGBA)
        glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS)
        #glutInitWindowSize(256,224)
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

    def get_direction(self):
        x_vec, y_vec, z_vec = 0, 0, 0

        if self.mode == Mode.KEY_MODE: 
            # angles come from mouse movement, 3 degress of freedom
            x_vec = cos(radians(self.head.xangle))
            y_vec = cos(radians(self.head.yangle))
            z_vec = -1*cos(radians(self.head.zangle))

        if self.mode == Mode.IMU_MODE:
            # IMU is expected to be mounted sideways, roll is ignored, expects euler angles
            x_vec = cos(self.head.zangle) * cos(self.head.yangle)
            y_vec = sin(self.head.zangle) * cos(self.head.yangle)
            z_vec = sin(self.head.yangle)

        if self.mode == Mode.MPU_MODE:
            # TODO: MPU has 3 degress of freedom
            x_vec = sin(self.head.zangle)
            y_vec = -1* (sin(self.head.xangle)*cos(self.head.zangle))
            z_vec = -1* (cos(self.head.xangle)*cos(self.head.zangle))

        return x_vec, y_vec, z_vec


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
        distance = sqrt(
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

        x_vec, y_vec, z_vec = self.get_direction()
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
                
                x_vec*distance,
                y_vec*distance,
                z_vec*distance,

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
        self.draw_room()
        # rotate shape
        glRotatef(self.shape.zangle, 0, 0, 1)
        glRotatef(self.shape.yangle, 0, 1, 0)
        glRotatef(self.shape.xangle, 1, 0, 0)

        #if self.shape is not None:
            #self.draw_shape()

        if self.dots is not None:
            self.draw_points()

        glPopMatrix()


    def draw_room(self):
    
        glPushMatrix()
        #glColor3f(0.2, 0.5, 0.8)
        glScalef(50,50,200)
        #glTranslatef(0,0, -100)
        self.draw_cube()
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

    def draw_points(self):
        glLineWidth(self.line_width);
        
        # clear out points when neccassary 
        if (self.dots.is_clean_slate()):
            #self.points = []
            pass

	# decide if two new points are useful
        #print(point1, point2)
        point1, point2 = self.dots.get_last_two()
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
            distance = sqrt(
                (self.head.x - point2[0]/100) ** 2 +
                (self.head.y - point2[1]/100) ** 2 +
                (self.head.z - point2[2]/100) ** 2
            )

            sx, sy, sz = self.get_direction()
            # normalize the vector (will rescale with the distance we need to cover)
            ns = sqrt(sx*sx + sy*sy + sz*sz)
            #print(sx/ns, sy/ns, sz/ns, distance)

            # store points with updated location (deals with the redrawing problem later)
            self.points.append((self.head.x + point1[0]/100 - sx/ns*distance, self.head.y + point1[1]/100 - sy/ns*distance, point1[2]/100))
            self.points.append((self.head.x + point2[0]/100 - sx/ns*distance, self.head.y + point2[1]/100 - sy/ns*distance, point2[2]/100))


        # bail if no points
        if len(self.points) < 2:
            return

        # redraw all points (TODO: find way of just appending points instead of redrawing everything)
        self.draw_line()
        #self.draw_tube()
        #self.draw_circles()

    def draw_line(self):
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
        
    def draw_tube(self):
        point0 = self.points[0]
        for point in self.points[1:]:
            glPushMatrix()
            glLoadIdentity()

            #TODO: Apply rotation matrix here to rotate tube section in the direction of point - point0
            # i.e change the normal of the circle from (0,0,-1) (default) to point - point0 by applying a rotation
            #TODO: TRANSLATE ALL POINTS TO ORIGIN THEN ROTATE THEN TRANSLATE BACK! Currently rotations are about the camera? or some non 0,0,0 position

            dir_vec = (point[0] - point0[0], point[1] - point0[1], point[2] - point0[2])
            dir_len = sqrt(dir_vec[0]*dir_vec[0] +  dir_vec[1]*dir_vec[1] +  dir_vec[2]*dir_vec[2]) 
            dir_theta = 0
            dir_phi = 0
            if not (any(dir_vec) == 0):
                dir_theta = degrees(atan(dir_vec[1]/dir_vec[0]))
                dir_phi = degrees(asin(dir_vec[2]/dir_len))

            print(dir_vec)
            print(dir_theta - 0, dir_phi - 0)
            glRotatef(dir_theta, 1, 0, 0)
            glRotatef(dir_phi, 0, 1, 0)

            glBegin(GL_TRIANGLE_STRIP) 

            # pick colour based on depth
            red = ((point0[2] + point[2])%50)/50 # doesnt matter what we do here
            blue = 1 - (((point0[2] + point[2])%50)/50) # doesnt matter what we do here
            green = 0

            glColor3f(red,green,blue)

            # DRAW CIRCLE CONNECTING POINT FROM ONE CIRCLE TO THE OTHER
            for i in reversed(range(0,361, 30)):
                theta = i * pi/180.0

                x = 1 * cos(theta) + point[0]
                y = 1 * sin(theta) + point[1]
                z = point[2]*-1.5

                x0 = 1 * cos(theta) + point0[0]
                y0 = 1 * sin(theta) + point0[1]
                z0 = point0[2]*-1.5

                glVertex3f(x0,y0,z0)
                glVertex3f(x,y,z)

            glEnd()
            glPopMatrix()
            point0 = point

    def draw_circles(self):
        for point in self.points:
            glPushMatrix()
            #TODO: Apply rotation matrix here to rotate tube section in the direction of point - point0
            # i.e change the normal of the circle from (0,0,-1) (default) to point - point0 by applying a rotation
            glBegin(GL_LINE_LOOP) 

            # pick colour based on depth
            red = ((point[2])%50)/50 # doesnt matter what we do here
            blue = 1 - (((point[2])%50)/50) # doesnt matter what we do here
            green = 0

            glColor3f(red,green,blue)

            # DRAW CIRCLE CONNECTING POINT FROM ONE CIRCLE TO THE OTHER
            for i in reversed(range(0,361, 30)):
                theta = i * pi/180.0

                x = 0.5 * cos(theta) + point[0]
                y = 0.5 * sin(theta) + point[1]
                z = point[2]*-1.5
                glVertex3f(x,y,z)

            glEnd()
            glPopMatrix()



    def draw_cube(self):
        glBegin(GL_QUADS)
        #glNormal3f( 0.0,  0.0, 1.0)
        #glVertex3f(-1.0, -1.0, 1.0)
        #glVertex3f( 1.0, -1.0, 1.0)
        #glVertex3f( 1.0,  1.0, 1.0)
        #glVertex3f(-1.0,  1.0, 1.0)
        
        glColor3f(0.2, 0.5, 1.0)
        glNormal3f( 0.0,  0.0, -1.0)
        glVertex3f( 1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        glVertex3f( 1.0,  1.0, -1.0)
        
        glColor3f(0.4, 0.5, 0.8)
        glNormal3f(-1.0,  0.0,  0.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0,  1.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        
        glColor3f(0.2, 0.4, 0.8)
        glNormal3f( 1.0,  0.0,  0.0)
        glVertex3f( 1.0, -1.0,  1.0)
        glVertex3f( 1.0, -1.0, -1.0)
        glVertex3f( 1.0,  1.0, -1.0)
        glVertex3f( 1.0,  1.0,  1.0)
        
        glColor3f(0.2, 0.2, 0.8)
        glNormal3f( 0.0,  1.0,  0.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glVertex3f( 1.0,  1.0,  1.0)
        glVertex3f( 1.0,  1.0, -1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        
        glColor3f(0.5, 0.5, 0.8)
        glNormal3f( 0.0, -1.0,  0.0)
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f( 1.0, -1.0, -1.0)
        glVertex3f( 1.0, -1.0,  1.0)
        glVertex3f(-1.0, -1.0,  1.0)
        glEnd()




if __name__ == "__main__":
    thing = View()
    thing.run()
