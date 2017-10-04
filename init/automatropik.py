#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
automatisation de la position des kinects.
Functional modes
@author: BIOGENE

"""
# TODO : à enlever si obsolete

global total_dic
global dist_inter_kinect
dist_inter_kinect=600

global rx ,ry
rx = 1
ry = 1
global taille_ecran
taille_ecran=(800 , 800)
print "taill", taille_ecran
global x_mouse , y_mouse
x_mouse=0
y_mouse=0

#sys.path.append('..')
#from parametres_vasarely import  p, volume , info_kinects,d_y, d_z,d_x

import sys
x = int(sys.argv[1])*100.0
y = int(sys.argv[2])*100.0
print "dim en cm de x , y = ", x, y

from pyglet.window import Window
win_0 = Window(screen=0, fullscreen=False, resizable=True, vsync = True)
win_0.set_size(taille_ecran[0],taille_ecran[1] )
import pyglet.gl as gl
import pyglet as pyglet

def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
#    gl.glEnable(gl.GL_BLEND)
#    gl.glShadeModel(gl.GL_SMOOTH)
#    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
#    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_DONT_CARE)# gl.GL_NICEST)#
#    gl.glDisable(gl.GL_DEPTH_TEST)
#    gl.glDisable(gl.GL_LINE_SMOOTH)
#    gl.glColor3f(1.0, 1.0, 1.0)
#    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glFrustum (-1.0, 1.0, -1.0, 1.0, 0.5, 2000.0)
    gl.glMatrixMode (gl.GL_MODELVIEW)
#    gl.gluOrtho2D(-100.0, x + 100, -100.0, x + 100)
    gl.gluLookAt (x / 2.0, y/2.0, 1000, x / 2.0, y/2.0, 0.0, 0.0, 1.0, 0.0)

win_0.on_resize = on_resize
#win_0.on_draw = on_draw

win_0.set_visible(True)
gl.glMatrixMode(gl.GL_MODELVIEW)
gl.glLoadIdentity()

gl.glClearColor(0.0, 0.0, 0.0, 0.0)

gl.glShadeModel(gl.GL_FLAT)

def drawOneLine(x1, y1,z1, x2, y2,z2 ):
  gl.glBegin(gl.GL_LINES)
  gl.glVertex3f(x1, y1,z1)
  gl.glVertex3f(x2, y2,z2)
  gl.glEnd()

def decors():
    label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=66,
                          x=win_0.width//2, y=-100,
                          anchor_x='center', anchor_y='center')
    global total_dic
    label.draw()
    kinect_place={}
#    total_dic={}
    gl.glColor3f(1.0, 1.0, 1.0)
    gl.glLineWidth (1)
#    global x,y
#    print x,y
#    x = 100#        global x_mouse , y_mouse
#        x_mouse=x
#        y_mouse=y
#        changepv()
#
#def changepv():
#    y = 100
    drawOneLine(0,0,-500,0,0,500)

    drawOneLine(0 , 0, 0, 0 , y , 0)
    drawOneLine(0 , y, 0 ,x , y , 0)
    drawOneLine(x , 0, 0 ,x , y , 0)
    drawOneLine(0 ,0, 0 ,x , 0 , 0)
#{'address':'10.42.0.11', 'port': 9999, 'x':8.0, 'y':d_y, 'z': 1.3, 'az':9*pi/6 ,'max':475},#3
    total_dic=[]

    if (y > 600):
        lenght = int (y / 2)
    else :
        lenght = y
    if (lenght>600):
        lenght = 600
    for k in range (100 , int(x) , dist_inter_kinect) :
        address = "10.42.0.1"+str(int( (k-100)/(dist_inter_kinect*2)) )
        port = str(9998+( (k-100)/dist_inter_kinect - ((k-100)/(dist_inter_kinect*2))*2) )
#        print address,port
        gl.glColor4f(0, 0, 1, 1)
        gl.glPointSize (16.0)
        gl.glBegin (gl.GL_POINTS)
        gl.glVertex2f(k, 0)
        gl.glEnd()
        if (k==100) or (k== 100+dist_inter_kinect*2) or (k== 100+dist_inter_kinect*4) or (k==100+dist_inter_kinect*6) or (k==100+dist_inter_kinect*8) :
            drawOneLine(k,0,0, k+cos (3*pi/6)*lenght, sin(3*pi/6)*lenght, 0)
            total_dic.append({'address':address,'port':port,'x':float(k/100),'y':0,'z':1.3,'az':3*pi/6,'max':lenght })
        else :
            drawOneLine(k,0,0, k+cos(pi/6)*dist_inter_kinect, sin(pi/6)*dist_inter_kinect, 0)
            total_dic.append({'address':address,'port':port,'x':float(k/100),'y':0,'z':1.3,'az':pi/6,'max':dist_inter_kinect })
            drawOneLine(k,0,0, k+cos (3*pi/6)*lenght, sin(3*pi/6)*lenght, 0)
            total_dic.append({'address':address,'port':port,'x':float(k/100),'y':0,'z':1.3,'az':3*pi/6,'max':lenght })
            drawOneLine(k,0,0, k+cos (5*pi/6)*dist_inter_kinect, sin(5*pi/6)*dist_inter_kinect, 0)
            total_dic.append({'address':address,'port':port,'x':float(k/100),'y':0,'z':1.3,'az':5*pi/6,'max':dist_inter_kinect })
    if (y > 700):
        for k in range (100 , int(x) , dist_inter_kinect)  :
            gl.glColor4f(0, 1, 0, 1)
            gl.glPointSize (16.0)

            gl.glBegin (gl.GL_POINTS)
            gl.glVertex2f(k, y)
            gl.glEnd()
#          drawOneLine(k['x']*100 ,k['y']*100, k['x']*100 + cos (k['az'])*k['max'],k['y']*100 + sin (k['az'])*k['max'])
            if (k==100) or (k== 100+dist_inter_kinect*2) or (k== 100+dist_inter_kinect*4) or (k==100+dist_inter_kinect*6) or (k==100+dist_inter_kinect*8) :
                drawOneLine(k,y,0, k+cos(9*pi/6)*lenght, y  + sin(9*pi/6)*lenght, 0)
            else :
                drawOneLine(k,y,0, k+cos(7*pi/6)*dist_inter_kinect, y+sin(7*pi/6)*dist_inter_kinect, 0)
                drawOneLine(k,y,0, k+cos(9*pi/6)*lenght, y+sin (9*pi/6)*lenght, 0)
                drawOneLine(k,y,0, k+cos(11*pi/6)*dist_inter_kinect, y+sin(11*pi/6)*dist_inter_kinect, 0)

    gl.glColor4f(1, 1, 1, 1)
    gl.glPointSize (8.0)
    gl.glBegin (gl.GL_POINTS);
    gl.glVertex2f(x, y -100)
    gl.glVertex2f(x, 0 +100)
    gl.glVertex2f(x, y/2)
    gl.glEnd()
    drawOneLine(x ,y/2,0 ,0 ,y/2 , 0 )
    drawOneLine(x ,y-100,0 ,0 ,y/2 , 0 )
    drawOneLine(x ,0+100,0 ,0 ,y/2 , 0 )

    gl.glFlush ()
#    for dico in total_dic :
#        print dico

from math import cos, sin,pi
from pyglet.window import mouse

#@win_0.event
#def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
#
#    if buttons & mouse.LEFT:
#        print "oyeeeeeeeeeeeee", x ,y

#        print "changepv"
#        gl.glLoadIdentity()
#        gl.glTranslatef(0, 0, -4)
#        gl.glRotatef(x_mouse, 0, 0, 1)
#        gl.glRotatef(x_mouse, 0, 1, 0)
#        gl.glRotatef(x_mouse, 1, 0, 0)



@win_0.event
def on_draw():
    win_0.clear()
    gl.glLineWidth ( 1 )
    gl.glLoadIdentity()
    gl.glFrustum (-50.0, 50.0, -50.0, 50.0, 30.5,7000.0)
    gl.glMatrixMode (gl.GL_MODELVIEW)
#    gl.gluLookAt (  sin(rx)*(x/2) + (x/2) ,cos(rx) *(x/2) + (y/2) , 2000+ cos(ry)*2000, x / 2.0, y/2.0, 0, 0, 0, 1.0)
#    gl.gluLookAt ( x / 2.0, y/2.0  , 2000, x / 2.0, y/2.0, 0, cos(ry), sin(ry), 1)
    gl.gluLookAt ( x / 2.0, y/2.0  , 2000, x / 2.0, y/2.0, 0, 0,1, 0)

    decors()

#    display_player()

def callback(dt):
    global rx, ry, rz
    rx += dt/1
    rx %= 6.28
    ry += dt/10
    ry %= 6.28
#    print '%f seconds since last callback' % dt , '%f  fps' % pyglet.clock.get_fps()

pyglet.clock.schedule(callback)
pyglet.app.run()
import datetime
for dico in total_dic :
    print dico
print total_dic
f = open("new_parametres.py" , 'w')
f.writelines("#!/usr/bin/env python \n")
f.writelines("# -*- coding: utf-8 -*- \n")
f.writelines("# FICHIER PARAMETRES TROPIQUE  : " + str(datetime.date.today()) + "\n")
#f.writelines()
f.writelines("info_kinects = [ \n")
for kinect in total_dic :
    f.writelines(str(kinect) + ", \n")
f.writelines("               ] \n")


#f.writelines(str(total_dic))

print 'Goodbye'

