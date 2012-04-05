#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Particle-like simulations using pure pyglet

"""
DEBUG = False
DEBUG = True
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
    print 'Screen %d: %dx%d at (%d,%d)' % (i, screen.width, screen.height, screen.x, screen.y)
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
scenario = 'calibration-grille'
scenario = 'calibration'#
scenario = 'rotating-circle', 
scenario = 'N-body'
scenario = 'gray-scott'#
#N = 256
N = 128
#N = 64
#N = 32
#N#N = 1024
from scenarios import Scenario
s = Scenario(N, scenario, volume, VPs)

# Window information
# ------------------
from pyglet.window import Window
wins = []
for i_screen, screen in enumerate(screens):
    if ((N_screen==1) and (i_screen==0)) or ((N_screen>1) and (i_screen==1)): 
        wins.append(Window(screen=screens[i_screen], fullscreen=(N_screen>1)))
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

win_0 = wins[0]
@win_0.event
def on_draw():
    global s
    s.do_scenario()
    win.clear()
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    gl.gluPerspective(VPs[0]['foc'], 1.0*win_0.width/win_0.height,
                      VPs[0]['pc_min'], VPs[0]['pc_max'])
    gluLookAt(VPs[0]['x'], VPs[0]['y'], VPs[0]['z'],
          VPs[0]['cx'], VPs[0]['cy'], VPs[0]['cz'], 0., 0, 1.0)
#    gl.glColor3f(1.0, 0., 0.)
    pyglet.graphics.draw(s.N, gl.GL_POINTS, ('v3f', s.particles[0:3, :].T.ravel().tolist()))

if N_screen>1:
    win_1 = wins[1]
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
        pyglet.graphics.draw(s.N, gl.GL_POINTS, ('v3f', s.particles[0:3, :].T.ravel().tolist()))

if N_screen>2:
    win_2 = wins[2]
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
        pyglet.graphics.draw(s.N, gl.GL_POINTS, ('v3f', s.particles[0:3, :].T.ravel().tolist()))

#win_3=wins[3]
#@win_3.event
#def on_draw():
#    win.clear()
#    gl.glColor3f(1., 1., 1.)
#    pyglet.graphics.draw(s.N, gl.GL_POINTS, ('v3f', s.particles[0:3, :].T.ravel().tolist()))

def callback(dt):
    try :
        if DEBUG: print '%f seconds since last callback' % dt , '%f  fps' % int(1/dt)
    except :
        pass
pyglet.clock.schedule(callback)
#pyglet.clock.schedule(lambda dt: None)
pyglet.app.run()
print 'Goodbye'
