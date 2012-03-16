#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Particle-like simulations using pyglet and a ugly bitmat - to convert to pure opengl

"""
import numpy as np
# Screen information
# ------------------
from parametres import VPs, volume

#import ctypes
import pyglet
import pyglet.gl as gl
from pyglet.window import Window
from pyglet.gl.glu import gluLookAt
#from shader import Shader
platform = pyglet.window.get_platform()
display  = platform.get_default_display()
screens  = display.get_screens()
screen   = screens[0]
N_screen = len(screens) # number of screens
#N_screen = 1 # uncomment to force display on one screen only
#N_screen = 2 # uncomment to force display on one screen only
if N_screen < len(screens): screens = screens[:N_screen]
# Parameters
# ----------
downscale = 1 # to debug
# downscale = 1 # the real stuff / beware the segmentation fault
# x, l’axe long, y l’axe transversal, z la hauteur
N_Y, N_Z = int(screen.width//downscale), int(screen.height//downscale) # size of the simulation grid
#print 'HACK ', N_Y, N_Z
# ---------
# Scenarios
# ---------
scenario = ['rotating-circle']#, 
scenario = ['calibration']#
scenario = ['gray-scott']#
scenario = ['calibration-grille']
N = 500
# N = 1024
from scenarios import Scenario
s = Scenario(N, scenario, VPs)
t_last = s.t # last time we changed scenario

# Screen information
# ------------------
wins = []
for i_screen, screen in enumerate(screens):
    wins.append(Window(screen=screens[i_screen], fullscreen=True))

def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    gl.glEnable(gl.GL_BLEND)
    gl.glShadeModel(gl.GL_SMOOTH)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_NICEST)
    gl.glDisable(gl.GL_DEPTH_TEST)

switch_rgb = (s.scenario == 'calibration') or (s.scenario == 'calibration-grille')

for i_win, win in enumerate(wins):
    win.on_resize = on_resize
    win.set_visible(True)

    @win.event
    def on_draw():
        global s, N_Y, N_Z
        s.do_scenario()
        win.clear()
        gl.glColor3f(1.0, 1.0, 1.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.gluPerspective(VPs[i_win]['foc'], 1.0*win.width/win.height, 0.01, 1000.0)
        c_x, c_y, c_z = s.center
        gluLookAt(VPs[i_win]['x'], VPs[i_win]['y'], VPs[i_win]['z'],
                  VPs[i_win]['cx'], VPs[i_win]['cy'], VPs[i_win]['cz'],
                  0., 0, 1.0)
        pyglet.graphics.draw(s.N, gl.GL_POINTS, ('v3f', s.particles[0:3, :].T.ravel().tolist()))

pyglet.clock.schedule(lambda dt: None)
pyglet.app.run()
print 'Goodbye'
