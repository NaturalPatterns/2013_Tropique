#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Particle-like simulations using pyglet.app

Exploration mode.

"""

#import sys
#window = pyglet.window.Window(fullscreen='-fs' in sys.argv, config=config)
from parametres import VPs, volume, p, kinects

do_sock = False
#do_sock=True

if do_sock:
    from network import Kinects
    k = Kinects(kinects)
else:
    positions = None

try:
    caca
    from parametres import sliders
    fig = sliders(s.p)
except Exception, e:
    print('problem while importing sliders ! Error = ', e)

# Window information
# ------------------
import pyglet
#pyglet.options['darwin_cocoa'] = True
platform = pyglet.window.get_platform()
print "platform" , platform
display = platform.get_default_display()
print "display" , display
screens = display.get_screens()
print "screens" , screens
for i, screen in enumerate(screens):
    print 'Screen %d: %dx%d at (%d,%d)' % (i, screen.width, screen.height, screen.x, screen.y)
#screen   = screens[0]
N_screen = 1# len(screens) # number of screens
assert N_screen == 1 # we should be running on one screen only

from scenarios import Scenario
s = Scenario(p['N'], 'leapfrog', volume, VPs, p)
#s = Scenario(p['N'], 'leapfrog', volume, [VPs[0]], p)

from pyglet.window import Window
from pyglet import clock

win_0 = Window(screen=screens[0], fullscreen=True)#  False, resizable=True)

import pyglet.gl as gl
from pyglet.gl.glu import gluLookAt
import numpy as np
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    gl.glEnable(gl.GL_BLEND)
    gl.glShadeModel(gl.GL_SMOOTH)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_DONT_CARE)# gl.GL_NICEST)#
    gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glDisable(gl.GL_LINE_SMOOTH)
    gl.glColor3f(1.0, 1.0, 1.0)
    gl.glDisable(gl.GL_CLIP_PLANE0)
    gl.glDisable(gl.GL_CLIP_PLANE1)
    gl.glDisable(gl.GL_CLIP_PLANE2)
    gl.glDisable(gl.GL_CLIP_PLANE3)


i_win = 0
win_0.on_resize = on_resize
win_0.set_visible(True)
win_0.set_mouse_visible(False)
gl.glMatrixMode(gl.GL_MODELVIEW)
gl.glLoadIdentity()
gl.gluPerspective(VPs[i_win]['foc'], 1.0*win_0.width/win_0.height, VPs[i_win]['pc_min'], VPs[i_win]['pc_max'])
gluLookAt(VPs[i_win]['x'], VPs[i_win]['y'], VPs[i_win]['z'],
      VPs[i_win]['cx'], VPs[i_win]['cy'], VPs[i_win]['cz'],
      0., 0, 1.0)
#win_0.on_draw = on_draw
# batch = pyglet.graphics.Batch()

fps_text = pyglet.clock.ClockDisplay()

##if DEBUG: fps_display = pyglet.clock.ClockDisplay(color=(1., 1., 1., 1.))
@win_0.event
def on_draw():
    global s

    if do_sock:
        positions = k.read_sock() # TODO: c'est bien une liste de coordonnées [x, y, z] ?
    else:
        from numpy import cos, pi, sqrt
# HACK pour simuler ROGER:
        positions = []
#        positions = [[s.center[0], s.center[1], s.center[2]]] # une personne fixe
        T = 20. # periode en secondes
        phi = 10/9. #.5*( 1 + sqrt(5) )
        positions.append([s.center[0], s.center[1] * (1. + 1.2*cos(2*pi*s.t/T)), 1.2*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
        positions.append([s.center[0], s.center[1] * (1. + 1.2 + .0*cos(2*pi*s.t/T/phi)), 1.2*s.center[2]]) # une autre personne dans un mouvement en phase
#        positions.append([s.center[0], s.center[1] * (1. + .0*cos(2*pi*s.t/T/phi)), 1.*s.center[2]]) # une autre personne dans un mouvement en phase
#        positions.append([s.center[0], s.volume[1]*.75, s.volume[2]*.75]) # une personne dans un mouvement circulaire (elipse)
#        positions.append([s.center[0], s.volume[1]*.25, s.volume[2]*.25]) # une autre personne dans un mouvement en phase
#    print positions
    s.do_scenario(positions=positions)

    win_0.clear()
    gl.glLineWidth (p['line_width'])
    gl.glColor3f(1.,1.,1.)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    gl.gluPerspective(VPs[0]['foc'], 1.0*win_0.width/win_0.height,
                      VPs[0]['pc_min'], VPs[0]['pc_max'])
    gluLookAt(VPs[0]['x'], VPs[0]['y'], VPs[0]['z'],
          VPs[0]['cx'], VPs[0]['cy'], VPs[0]['cz'], 0., 0, 1.0)

    pyglet.graphics.draw(2*s.N, gl.GL_LINES, ('v3f', s.particles[0:6, :].T.ravel().tolist()))
    
    for position in positions:
        gl.glPointSize(10)
        gl.glColor3f(1.,0.,0.)
        pyglet.graphics.draw(1, gl.GL_POINTS, ('v3f', position))
        

    fps_text.draw()
#     batch.draw()


    if do_sock: k.trigger()

def callback(dt):
    global do_sock
    try :
        if DEBUG: print '%f seconds since last callback' % dt , '%f  fps' % pyglet.clock.get_fps()
    except :
        pass

#dt = 1./40 # interval between 2 captations
#pyglet.clock.schedule_interval(callback, dt)
pyglet.clock.schedule(callback)
#pyglet.clock.schedule(lambda dt: None)
pyglet.app.run()
print 'Goodbye'

# Retained mode
# -------------
# 
# Retained mode rendering stores vertex and index data in vertex buffer objects
# (or vertex arrays if the context does not support VBOs), and renders multiple
# primitives in a single batch operation.  This permits the highest-performance
# rendering possible with pyglet.
# 
# To use retained mode, create a Batch object::
# 
#     batch = graphics.Batch()
#     
# Then add any number of primitives to the batch object.  Conceptually, a batch
# object is similar to a display list, except that the primitives can be
# modified or removed after they have been added, and the batch object performs
# better than display lists on current generation hardware.
# 
# For example, to add the shaded triangle from the previous example to the batch
# object::
# 
#     batch.add(3, GL_TRIANGLES,
#         ('v2f', [10., 10., 
#                  40., 10., 
#                  40., 40.]),
#         ('c3b', [255, 0, 0,
#                  0, 255, 0,
#                  0, 0, 255]))
# 
# The `add` method actually returns a `Primitive` object, which can subsequently
# be modified.  In fact, no initial data for the primitive needs to be given at
# all.  The following is equivalent to the previous example::
# 
#     prim = batch.add(3, GL_TRIANGLES, 'v2f', 'c3b')
#     prim.vertices = [10., 10.,
#                      40., 10.,
#                      40., 40.]
#     prim.colors = [255, 0, 0,
#                    0, 255, 0,
#                    0, 0, 255]
# 
# The `vertices` and `colors` arrays can also be modified in-place::
# 
#     prim.vertices[0] += 1.
# 
# To draw the batch object::
# 
#     batch.draw()
# 
# No guarantee about the order of rendering is given for the primitives inside a
# batch object.  They may be re-ordered for efficiency reasons.  A 2D
# application would typically use one batch object for each "layer" of
# rendering; a 3D application could use one batch object for all 3D objects with
# the depth buffer enabled.
# 

