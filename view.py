from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import numpy
import math

import head
import shape

class View:
    def __init__(self, head, shape):
        # GLUT initialization in program global, so initialize it on
        # the process level. It might be
        glutInit(sys.argv)

        self.head = head
        self.shape = shape
        self.fps = 60

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
        self.draw()

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

                # what we're looking at
                #math.sin(self.head.xangle) * math.cos(self.head.zangle * -1),
                #math.cos(self.head.zangle) * math.sin(self.head.zangle * 1),
                #math.sin(self.head.xangle) - 1,

                #math.sin(self.head.xangle)*distance,
                #-1*math.sin(self.head.yangle)*math.cos(self.head.xangle)*distance,
                #-1*math.cos(self.head.yangle)*math.cos(self.head.xangle)*distance - 1,

                math.cos(self.head.zangle)*math.cos(self.head.yangle),
                math.sin(self.head.zangle)*math.cos(self.head.yangle),
                math.sin(self.head.yangle) - 1,

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

        self.draw_shape()

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


if __name__ == "__main__":
    thing = View()
    thing.run()
