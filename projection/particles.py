#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Particle-like simulations using pyglet and a ugly bitmat - to convert to pure opengl

"""
import numpy as np
# Screen information
# ------------------
import ctypes
import pyglet
import pyglet.gl as gl
from shader import Shader
platform = pyglet.window.get_platform()
display  = platform.get_default_display()
screens  = display.get_screens()
screen   = screens[0]
N_screen = len(screens) # number of screens
#N_screen = 1 # uncomment to force display on one screen only
#N_screen = 2 # uncomment to force display on one screen only
if N_screen<len(screens): screens = screens[:N_screen]
# Parameters
# ----------
downscale = 2 # to debug
# downscale = 1 # the real stuff / beware the segmentation fault
# x, l’axe long, y l’axe transversal, z la hauteur
N_Y, N_Z = int(screen.width//downscale), int(screen.height//downscale) # size of the simulation grid
#print 'HACK ', N_Y, N_Z
# ---------
# Scenarios
# ---------
scenarios = ['gray-scott'] # ['calibration', 'calibration-grille', 'rotating-circle']#, 'flock', 'navier-stokes']
i_scenario = 0 # initial scenario chosen
t_scenario = 10 # time to switch scenarios
#t_scenario = 4e99 # leave uncommented to avoid changing

N = 2048
N = 512
#N = 16
from scenarios import Scenario
s = Scenario(N, scenarios[i_scenario])
t_last = s.t # last time we changed scenario

# Screen information
# ------------------

if N_screen>1: 
    win_1 = pyglet.window.Window(screen=screens[0], fullscreen=True)
    win_2 = pyglet.window.Window(screen=screens[1], fullscreen=True)
    if N_screen>2: win_3 = pyglet.window.Window(screen=screens[2], fullscreen=True)
else:
    win_1 = pyglet.window.Window(screen=screens[0], resizable=True, width=N_Y, height=N_Z, fullscreen=False)
    print 'Running in single window mode '

#dt = 1.

image = np.ones((N_Z,N_Y,4), dtype=np.float32)
data = image.ctypes.data
texture_data = pyglet.image.Texture.create_for_size(
    gl.GL_TEXTURE_2D, N_Y, N_Z, gl.GL_RGBA32F_ARB)
gl.glBindTexture(texture_data.target, texture_data.id)
gl.glTexParameteri(texture_data.target, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
gl.glTexParameteri(texture_data.target, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
gl.glTexImage2D(texture_data.target, texture_data.level, gl.GL_RGBA32F_ARB,
                N_Y, N_Z, 0, gl.GL_RGBA, gl.GL_FLOAT, data)
gl.glBindTexture(texture_data.target, 0)

# Framebuffer
# -----------
framebuffer = gl.GLuint(0)
gl.glGenFramebuffersEXT(1, ctypes.byref(framebuffer))
gl.glBindFramebufferEXT(gl.GL_FRAMEBUFFER_EXT, framebuffer)
gl.glFramebufferTexture2DEXT(gl.GL_FRAMEBUFFER_EXT, gl.GL_COLOR_ATTACHMENT0_EXT,
                             gl.GL_TEXTURE_2D, texture_data.id, 0);
gl.glBindFramebufferEXT(gl.GL_FRAMEBUFFER_EXT, 0)

# Color shader
# ------------
vertex_shader   = open('./color.vert').read()
fragment_shader = open('./color.frag').read()
color_shader    = Shader(vertex_shader, fragment_shader)

color_shader.bind()
color_shader.uniformi('texture', 0)
color_shader.unbind()
switch_rgb = (s.scenario == 'calibration') or (s.scenario == 'calibration-grille')

win_1.set_visible(True)
@win_1.event
def on_draw():
    global s, i_scenario, t_last, N_Y, N_Z
    
    if switch_rgb: 
        gl.glColor3f(1.0, 0., 0.)
    else:
        gl.glColor3f(1.0, 1.0, 1.0)
    gl.glClearColor(1.0,1.0,1.0,1.0)
    win_1.clear()
    s.do_scenario()
    if (s.t - t_last) > t_scenario: 
        i_scenario +=1
        i_scenario %= len(scenarios)
        s.scenario = scenarios[i_scenario]
        print 'switching to ', scenarios[i_scenario]
        t_last = s.t

    data = s.projection(0, N_Y=N_Y, N_Z=N_Z).ctypes.data
    gl.glTexImage2D(texture_data.target, texture_data.level, gl.GL_RGBA32F_ARB,
                    N_Y, N_Z, 0, gl.GL_RGBA, gl.GL_FLOAT, data)
    gl.glViewport(0, 0, win_1.width, win_1.height)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(0, 1, 0, 1, -1, 1)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    color_shader.bind()
    texture_data.blit(x=0.0, y=0.0, width=1.0, height=1.0)

if N_screen>1:
    win_2.set_visible(True)
    @win_2.event
    def on_draw():
        gl.glClearColor(1.0,1.0,1.0,1.0)
        win_2.clear()
        if switch_rgb: gl.glColor3f(0., 1.0, 0.)
        data = s.projection(1, N_Y=N_Y, N_Z=N_Z).ctypes.data
        gl.glTexImage2D(texture_data.target, texture_data.level, gl.GL_RGBA32F_ARB,
                        N_Y, N_Z, 0, gl.GL_RGBA, gl.GL_FLOAT, data)
        gl.glViewport(0, 0, win_2.width, win_2.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, 1, 0, 1, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        color_shader.bind()
        texture_data.blit(x=0.0, y=0.0, width=1.0, height=1.0)

if N_screen>2:
    win_3.set_visible(True)
    @win_3.event
    def on_draw():
        gl.glClearColor(1.0,1.0,1.0,1.0)
        win_3.clear()
        if switch_rgb: gl.glColor3f(0., 0., 1.0)
        data = s.projection(2, N_Y=N_Y, N_Z=N_Z).ctypes.data
        gl.glTexImage2D(texture_data.target, texture_data.level, gl.GL_RGBA32F_ARB,
                        N_Y, N_Z, 0, gl.GL_RGBA, gl.GL_FLOAT, data)
        gl.glViewport(0, 0, win_3.width, win_3.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, 1, 0, 1, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        color_shader.bind()
        texture_data.blit(x=0.0, y=0.0, width=1.0, height=1.0)

#pyglet.clock.schedule_interval(lambda dt: None, 1.0/60.0)
pyglet.clock.schedule(lambda dt: None)
pyglet.app.run()
print 'Goodbye'
