#!/bin/python2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from head import Head
import numpy as np
from math import sin,cos,tan,radians,pi
import DepthSense as ds

zmov = 0
xmov = 0
prevz = 0
prevx = 0 
theta = pi/2
phi = 0

def on_timer(value=0):
        glutPostRedisplay();
        glutTimerFunc(1000/60, on_timer, value + 1)


def initFun():

    # Create window
    glutInit()    
    glutInitWindowSize(640,480)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
    glEnable(GL_DEPTH_TEST)
    glutCreateWindow("Point Cloud")

def cameraFun():

    # Create Camera
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glViewport(0, 0, 640, 480)
    #glClearDepth(1) 
    #glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    gluPerspective(45, 640.0/480.0, 0.1, 2000) 
    gluLookAt(0,0,1, 
            sin(theta)*cos(phi),
            sin(theta)*sin(phi),
            cos(theta) - 1, 
            0,1,0) 

    #gluOrtho2D(0.0,400.0,0.0,400.0)
    #glOrtho(-320,320,-240,240,0.1,1000)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0, 0.0)
    glPointSize(3.0)

def motionFun(x, y):
    #print "moving x: ", x, " moving y: ", y
    global zmov, prevz, theta
    global xmov, prevx, phi 
    print "moving x: ", xmov, " moving y: ", zmov

    xmov = x/640.0 * pi
    zmov = y/480.0 * pi

    theta = zmov
    phi = xmov



def keyFun(key, x, y):
    print "key x: ", x, " key y: ", y, " w/e: ", key
         
def displayFun():
    
    cameraFun()

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    vertex = ds.getVertices()
    sync = ds.getSyncMap()
    print ds.getAcceleration()

    glPushMatrix()
    glBegin(GL_POINTS)
    for i in range(0,240):
        for j in range(0, 320):
            v = vertex[i][j]
            c = sync[i][j]
            if ((not (all(v) == 0)) and \
                    (not (any(v) == 32001)) and \
                    (not (all(c) == 0))):
                glColor3ub(c[2],c[1], c[0])
                #glVertex3s(v[0], v[1], v[2])
                glVertex3s(v[0], v[1], v[2]*-1)
                #glVertex2s(v[0] + 320, v[1] + 240)
    glEnd()
    glPopMatrix()
    glutSwapBuffers()

if __name__ == '__main__':

    try:
        ds.initDepthSense()
        head = Head()

        initFun()
        glutPassiveMotionFunc(motionFun)
        glutKeyboardFunc(keyFun)
        glutDisplayFunc(displayFun)
        on_timer()
        glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS)
        glutMainLoop()
    finally:
        ds.killDepthSense()



