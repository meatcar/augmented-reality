#!/bin/python2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import DepthSense as ds
import numpy as np
ds.initDepthSense()

def on_timer(value=0):
        glutPostRedisplay();
        glutTimerFunc(1000//30, on_timer, value + 1)


def initFun():
    glMatrixMode(GL_PROJECTION)
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0, 0.0)
    glPointSize(1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    #gluOrtho2D(0.0,400.0,0.0,400.0)
    gluPerspective(45, 640.0/480.0, 0.1, 1000) 
    gluLookAt(0,0,1, 0,0,0, 0,1,0) 
    

    
def displayFun():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    vertex = ds.getVertices()
    sync = ds.getSyncMap()

    glBegin(GL_POINTS)
    for i in range(0,240):
        for j in range(0, 320):
            v = vertex[i][j]
            c = sync[i][j]
            if not(all(v) == 0) and not (any(v) == 32001):
                glColor3f(c[0]/255.0,c[1]/255.0, c[2]/255.0)
                #glVertex3s(v[0], v[1], v[2])
                glVertex3s(v[0], v[1], v[2]*-1)
                #glVertex2s(v[0] + 320, v[1] + 240)

      
    
    glEnd()
    glutSwapBuffers()
if __name__ == '__main__':
    glutInit()    
    glutInitWindowSize(640,480)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
    glEnable(GL_DEPTH_TEST)
    glutCreateWindow("Scatter")

    glutDisplayFunc(displayFun)

    initFun()
    on_timer()
    glutMainLoop()



