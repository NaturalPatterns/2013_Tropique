#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Particle-like simulations using pyglet

"""
import numpy as np
#def socket
import socket 
import time
t = time.time()
UDP_IP=""
UDP_PORT=3003
sock = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP
sock.bind( (UDP_IP,UDP_PORT) )
#sock.settimeout(0)
sock.setblocking(0)

global posx , posy , posz , mypos
posx=0
posy=0
posz=0
mypos=[posx, posy, posz]

def read_sock():
    try :	
        Donnee, Client = sock.recvfrom (128)
    except (KeyboardInterrupt):
        raise
    except:
       pass # detect = 0
    else :
#        print"data =" ,Donnee 
#        Donnee = Donnee [0: (len(Donnee) - 1)]
	#Donnee = ((angle + x + y + "o")*nbr_player)+";"
	datasplit = Donnee.split(";")
#	print "datasplit =" , datasplit
	store_blob = [[ int(each2) for each2 in each.split(",") ] for each in datasplit]
#	store_blob = [ int(each2) for each2 in datasplit[0].split(" ") ]
	#print "ras"
	return store_blob

def read_pos():
    global mypos
#    posx, posy = np.nan, np.nan
    try :
        a = read_sock()
    except:
        rien =0
    else:
        try:
            posy=float(a[0]) + 1196
            posx=float(a[1])
            posz=float(a[2])

            posx /=100
            posy /=100
            posz /=100
            posx = 2.0
            posy =15.0
            posz=3.5
            mypos=[posy, posx, posz]
        except:
#            print "ca va pas"
            rien = 0
        else:
            rien = 1
    return mypos #((float(posx))/90.0) + 2.1, ((float(posy))/90.0) + 2.1

# Screen information
# ------------------
from parametres import VPs, volume

import pyglet
pyglet.options['darwin_cocoa'] = True
platform = pyglet.window.get_platform()
print "platform" , platform
display = platform.get_default_display()
print "display" , display
screens = display.get_screens()
print "screens" , screens
for i, screen in enumerate(screens):
    print 'Screen %d: %dx%d at (%d,%d)' % (i,screen.width, screen.height, screen.x, screen.y)
#screen   = screens[0]
N_screen = len(screens) # number of screens
#N_screen = 1 # uncomment to force display on one screen only
#N_screen = 2 # uncomment to force display on one screen only
if N_screen < len(screens): screens = screens[:N_screen]

# Parameters
# ----------
downscale = 4 # to debug
downscale = 1 # the real stuff / beware the segmentation fault
# x, l’axe long, y l’axe transversal, z la hauteur
N_Y, N_Z = int(screen.width//downscale), int(screen.height//downscale) # size of the simulation grid
#print 'HACK ', N_Y, N_Z
# ---------
# Scenarios
# ---------
# scenario = 'rotating-circle', 
# scenario = 'calibration'#
#scenario = 'gray-scott'#
scenario = 'calibration-grille'
N = 500
# N = 1024
from scenarios import Scenario
s = Scenario(N, scenario, volume, VPs)

# Window information
# ------------------
from pyglet.window import Window
wins = []
for i_screen, screen in enumerate(screens):
    if i_screen>0:
        wins.append(Window(screen=screens[i_screen], fullscreen=True))
    #print('OpenGL version:', wins[i_screen].context.get_info().get_version())
    #print('OpenGL 3.2 support:', wins[i_screen].context.get_info().have_version(3, 2))

import pyglet.gl as gl
from pyglet.gl.glu import gluLookAt

def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    gl.glEnable(gl.GL_BLEND)
    gl.glShadeModel(gl.GL_SMOOTH)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_NICEST)
    gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glColor3f(1.0, 1.0, 1.0)

for i_win, win in enumerate(wins):
    win.on_resize = on_resize
    win.set_visible(True)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    gl.gluPerspective(VPs[i_win]['foc'], 1.0*win.width/win.height, VPs[i_win]['pc_min'], VPs[i_win]['pc_max'])
    gluLookAt(VPs[i_win]['x'], VPs[i_win]['y'], VPs[i_win]['z'],
          VPs[i_win]['cx'], VPs[i_win]['cy'], VPs[i_win]['cz'],
          0., 0, 1.0)
          

gl.glPointSize (10)

win_0=wins[0]
@win_0.event
def on_draw():
    global s
    global mypos
#    read_pos()
    mypos=[3, 2, 2]

    s.do_scenario(mypos)
    mypos=[3, 2, 2]
    print "mypos = ",mypos
    #       s.do_scenario()
    win.clear()
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    gl.gluPerspective(VPs[0]['foc'], 1.0*win_0.width/win_0.height, 
                      VPs[0]['pc_min'], VPs[0]['pc_max'])
    gluLookAt(VPs[0]['x'], VPs[0]['y'], VPs[0]['z'],
          VPs[0]['cx'], VPs[0]['cy'], VPs[0]['cz'], 0., 0, 1.0)
#    gl.glColor3f(1.0, 0., 0.)
    gl.glPointSize (10)

    pyglet.graphics.draw(s.N, gl.GL_POINTS, ('v3f', s.particles[0:3, :].T.ravel().tolist()))

if N_screen>1:
    win_1=wins[1]
    @win_1.event
    def on_draw():
        win.clear()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.gluPerspective(VPs[1]['foc'], 1.0*win_1.width/win_1.height, 
                      VPs[1]['pc_min'], VPs[1]['pc_max'])
        gluLookAt(VPs[1]['x'], VPs[1]['y'], VPs[1]['z'],
          VPs[1]['cx'], VPs[1]['cy'], VPs[1]['cz'], 0., 0, 1.0)
#        gl.glColor3f(0., 1.0, 0.)
        gl.glPointSize (10)

        pyglet.graphics.draw(s.N, gl.GL_POINTS, ('v3f', s.particles[0:3, :].T.ravel().tolist()))

if N_screen>2:
    win_2=wins[2]
    @win_2.event
    def on_draw():
        win.clear()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.gluPerspective(VPs[2]['foc'], 1.0*win_2.width/win_2.height, 
                      VPs[2]['pc_min'], VPs[2]['pc_max'])
        gluLookAt(VPs[2]['x'], VPs[2]['y'], VPs[2]['z'],
          VPs[2]['cx'], VPs[2]['cy'], VPs[2]['cz'], 0., 0, 1.0)
#        gl.glColor3f(0., 0., 1.0)
        gl.glPointSize (10)

        pyglet.graphics.draw(s.N, gl.GL_POINTS, ('v3f', s.particles[0:3, :].T.ravel().tolist()))
    
#win_3=wins[3]
#@win_3.event
#def on_draw():
#    win.clear()
#    gl.glColor3f(1., 1., 1.)
#    pyglet.graphics.draw(s.N, gl.GL_POINTS, ('v3f', s.particles[0:3, :].T.ravel().tolist()))
#pyglet.clock.schedule_interval(read_pos(), .5)
def callback(dt):
    try :
        print '%f seconds since last callback' % dt ,int(1/dt)
    except :
        pass
    read_pos()


pyglet.clock.schedule(callback)
pyglet.clock.schedule(lambda dt: None)
pyglet.app.run()
print 'Goodbye' 