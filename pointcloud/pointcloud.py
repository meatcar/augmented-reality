#!/bin/python2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from math import sin,cos,tan,radians,pi
import DepthSense as ds

zmov = 0
xmov = 0
angle = 0

def on_timer(value=0):
        glutPostRedisplay();
        glutTimerFunc(1000/60, on_timer, value+1)

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    gluPerspective(45, float(w)/float(h), 0.1, 2000) 

def initFun():

    # Create window
    glutInit()    
    glutInitWindowSize(640,480)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow("Point Cloud")
    reshape(640,480)

def cameraFun():

    # Create Camera
    global angle
    angle += (2*pi/10.0)
    gluLookAt(0, 0, 0, 
            0,
            0,
            200, 
            0,1,0) 

    #gluOrtho2D(0.0,400.0,0.0,400.0)
    #glOrtho(-320,320,-240,240,0.1,1000)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0, 0.0)
    glPointSize(2.0)

def motionFun(x, y):
    #print "moving x: ", x, " moving y: ", y
    global zmov, prevz, theta
    global xmov, prevx, phi 

    zmov = (x) % 360
    xmov = (x) % 360

def keyFun(key, x, y):
    print "key x: ", x, " key y: ", y, " w/e: ", key
         
def displayFun():
    

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    cameraFun()

    glEnable(GL_DEPTH_TEST)
    glClearDepth(1)
    
    vertex = ds.getVertices()
    sync = ds.getSyncMap()

    glPushMatrix()
    glLoadIdentity()
    glBegin(GL_POINTS)
    for i in range(0,240):
        for j in range(0, 320):
            v = vertex[i][j]
            c = sync[i][j]
            if ((not (all(v) == 0)) and \
                    (not (any(v) == 32001)) and \
                    (not (all(c) == 0))):
                glColor3ub(c[2],c[1], c[0])
                glVertex3s(v[0], v[1], v[2]*2)
    glEnd()
    glPopMatrix()


    glutSwapBuffers()

if __name__ == '__main__':

    try:
        ds.initDepthSense()
        initFun()
        glutPassiveMotionFunc(motionFun)
        glutKeyboardFunc(keyFun)
        glutReshapeFunc(reshape)
        glutDisplayFunc(displayFun)
        glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS)
        on_timer()
        
        glutMainLoop()
    finally:
        ds.killDepthSense()



