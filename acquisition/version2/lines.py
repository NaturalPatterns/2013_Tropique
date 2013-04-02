#!/usr/bin/python

# This is statement is required by the build system to query build info
if __name__ == '__build__':
	raise Exception

'''
lines.c from the Redbook examples.  
Converted to Python by Jason L. Petrone 6/00

/*
 *  lines.c
 *  This program demonstrates geometric primitives and
 *  their attributes.
*/
OpenGL(R) is a registered trademark of Silicon Graphics, Inc.

'''
from math import pi , cos ,sin , tan

import sys
sys.path.append('../../projection/')
from parametres import info_kinects , d_y, d_z,d_x , VPs
print d_y, d_z,d_x , VPs

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print '''
ERROR: PyOpenGL not installed properly.  
        '''
  sys.exit()

def drawOneLine(x1, y1, x2, y2):
  glBegin(GL_LINES)
  glVertex2f(x1, y1)
  glVertex2f(x2, y2)
  glEnd()


def init():
  glClearColor(0.0, 0.0, 0.0, 0.0)
  glShadeModel(GL_FLAT)

def display():
  glClear(GL_COLOR_BUFFER_BIT)

  # select white for all lines
  glColor3f(1.0, 1.0, 1.0)
  drawOneLine(0 , 0, 0 , d_y*100)
  drawOneLine(0 , d_y*100, d_x*100 , d_y*100)
  drawOneLine(d_x*100 , 0, d_x*100 , d_y*100)
  drawOneLine(0 ,0, d_x*100 , 0)
  for k in info_kinects :
      glColor4f(0, 0, 1, 1);
      glPointSize (32.0);

      glBegin (GL_POINTS);
      glVertex2f(k['x']*100, k['y']*100);
      glEnd();
      drawOneLine(k['x']*100 ,k['y']*100, k['x']*100 + cos (k['az'])*k['max'],k['y']*100 + sin (k['az'])*k['max'])
  for p in VPs:
      glColor4f(0, 1, 1, 1);
      glPointSize (32.0);

      glBegin (GL_POINTS);
      glVertex2f(p['x']*100, p['y']*100);
      glEnd();
      drawOneLine(p['x']*100 ,p['y']*100, p['cx']*100 ,p['cy']*100 )      
  print "whooo"
  glFlush ()

def reshape(w, h):
  glViewport(0, 0, w, h)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  gluOrtho2D(-10.0, w, -10.0, h)

def keyboard(key, x, y):
  if key == chr(27):
    sys.exit(0)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(1800, 950)
glutInitWindowPosition(100, 100)
glutCreateWindow('Lines')
init()
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMainLoop()
