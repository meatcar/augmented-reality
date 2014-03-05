import sdl2

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

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
        if key is b'w':
            self.head.z -= 0.02
        elif key is b's':
            self.head.z += 0.02
        elif key is b'a':
            self.head.x -= 0.02
        elif key is b'd':
            self.head.x += 0.02
        elif key is b' ':
            print(head)

    def on_passive_motion(self, x, y):
        if self.mousex is None:
            self.mousex = x
        else:
            self.head.xangle += (self.mousex - x) / 100
            self.mousex = x

        if self.mousey is None:
            self.mousey = y
        else:
            self.head.yangle += (self.mousey - y) / 100
            self.mousey = y

