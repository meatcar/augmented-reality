from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from math import *
import sys

class KeyController:
    def __init__(self, head, shape):
        self.head = head
        self.shape = shape

        self.mousex = None
        self.mousey = None

        glutSpecialFunc(self.on_special)
        glutKeyboardFunc(self.on_keyboard)
        glutPassiveMotionFunc(self.on_passive_motion)

    def on_special(self, key, x, y):
        if key == GLUT_KEY_UP:
            self.head.y += 0.02
        elif key == GLUT_KEY_DOWN:
            self.head.y -= 0.02
        elif key == GLUT_KEY_LEFT:
            self.head.eye_distance -= 0.02
        elif key == GLUT_KEY_RIGHT:
            self.head.eye_distance += 0.02

    def on_keyboard(self, key, x, y):
        v = 0.02
        if key is b'w':
            self.head.x -= v * cos(radians(self.head.xangle))
            self.head.y -= v * cos(radians(self.head.yangle))
            self.head.z -= v * cos(radians(self.head.zangle))
        elif key is b's':
            self.head.x += v * cos(radians(self.head.xangle))
            self.head.y += v * cos(radians(self.head.yangle))
            self.head.z += v * cos(radians(self.head.zangle))
        elif key is b'a':
            self.head.x -= v
        elif key is b'd':
            self.head.x += v
        elif key is b' ':
            distance = sqrt(
                    (self.head.x - self.shape.x) ** 2 +
                    (self.head.y - self.shape.y) ** 2 +
                    (self.head.z - self.shape.z) ** 2
                    )
            print(self.head)
            print("looking at {},{},{}".format(
                    cos(radians(self.head.xangle)) * distance,
                    cos(radians(self.head.yangle)) * distance,
                    -1 * cos(radians(self.head.zangle)) * distance))
        elif key is b'q':
            sys.exit(0)

    def on_passive_motion(self, x, y):
        if self.mousex is None:
            self.mousex = x
        else:
            self.head.xangle += (self.mousex - x) / 5
            self.head.xangle = self.head.xangle % 360
            self.mousex = x

        if self.mousey is None:
            self.mousey = y
        else:
            self.head.yangle += (self.mousey - y) / 5
            self.head.yangle = self.head.yangle % 360
            self.mousey = y

