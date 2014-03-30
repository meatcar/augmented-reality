#!/bin/python2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import DepthSense as ds
import numpy as np
ds.initDepthSense()

def initFun():
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0, 0.0)
    glPointSize(1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0,640.0,0.0,480.0)
   
    
def displayFun():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)

    vertex = ds.getVertices()
    #sync = ds.getSyncMap()

    for i in range(0,240):
        for j in range(0, 320):
            v = vertex[i][j]
            #c = sync[i][j]
            #glColor3ub(c[0],c[1], c[2])
            print v
            glVertex2f(v[0]/100, v[1]/100)
      
    glEnd()
    glFlush()

if __name__ == '__main__':
    glutInit()    
    glutInitWindowSize(640,480)
    glutCreateWindow("Scatter")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    initFun()
    glutMainLoop()



