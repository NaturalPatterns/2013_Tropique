#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Particle-like simulations using pyglet

"""
import numpy as np
import time
t = time.time()
# Screen information
# ------------------
import ctypes
import pyglet
pyglet.options['debug_gl'] = False
import pyglet.gl as gl
from shader import Shader
platform = pyglet.window.get_platform()
display  = platform.get_default_display()
screens  = display.get_screens()
screen   = screens[0]
downscale = 4 # to debug
#downscale = 1 # the real stuff
N_X, N_Y = screen.width//downscale, screen.height//downscale # size of the simulation grid
N_Z = screen.width//downscale # depth
# Scenarios
# ---------
scenario = 'calibration'
#scenario = 'flock'
#scenario = 'navier-stokes'

N = 1024
#N = 16
particles = np.zeros((4, N), dtype=np.float32)
particles[0,:] = np.random.rand(N) * N_X
particles[1,:] = np.random.rand(N) * N_Y
particles[2:4,:] = np.random.randn(2,N) * .01 # speed is measured in screen size per second
#particles[2,:] = particles[1,:]
#particles[3,:] = -particles[0,:]
def do_scenario(particles, scenario):
    global t
    t_last = t
    t = time.time()  
    if scenario == 'calibration':
        particles[0,:], particles[1,:] = N_X/2, N_Y/2
        frequency = .1 # how fast the whole disk moves in Hz
        radius = .3 * N_Y
        N_dots = 16
        angle = 2 * np.pi *  frequency *  t + np.linspace(0, 2 * np.pi, N_dots)
        particles[0,:N_dots] = N_X/2 + radius * np.sin(angle)
        particles[1,:N_dots] = N_Y/2 + radius * np.cos(angle)

    elif scenario == 'flock':  
        # règle basique d'évitement
        for i in range(N):
            distance_moy = np.sqrt((particles[0,:] - particles[0, i])**2 + (particles[1,:] - particles[0, i])**2).mean()
            particles[2:4, i] += np.random.randn(2) *.001 * distance_moy
    #        particles[2:4, i] *= np.exp(- distance / 5. )
    #
        # règle basique de clustering des vitesses de particules proches
        for i in range(N):
            distance = np.sqrt((particles[0,:] - particles[0, i])**2 + (particles[1,:] - particles[0, i])**2)
            weights = np.exp(- distance**2 /2 / .1**2 )
            weights /= weights.sum()
    #        particles[2:4, i] *= np.random.randn(2) *.001 * distance
    #        particles[2:4,:] *= .99
            particles[2:4, i] += .01 * (particles[2:4, i] - (particles[2:4, :] * weights).sum() )
    
        particles[0:2,:] += (t - t_last ) *  particles[2:4,:]
        particles[2:4,:] += np.random.randn(2,N) *.0001
        particles[2:4,:] *= .99


    particles[0,:] = np.mod(particles[0,:], N_X)
    particles[1,:] = np.mod(particles[1,:], N_Y)
    
    return particles


# Projection information
# ----------------------
# taille du plan de reference
width, height = 8, 8*N_Y/N_X # en metres
# position spatiale des VPs par rapport au centre du plan de reference
#(x, y, z) du centre = (0, 0, 0), z est la profondeur
x_VPs = [ -3., 0., 3. ] # en metres; placement regulier
y_VPs = [ 0., 0., 0.] # en metres; on a place les VPs a la hauteur du centre du plan de reference
z_VPs = [ 8., 8., 8. ]

def projection(particles, i_VP):

    image = np.ones((N_Y,N_X,4), dtype=np.float32)
    for i in range(N):
        image[np.floor(particles[1, i]), np.floor(particles[0, i]), :] = 0.

# Screen information
# ------------------
n_screens = len(screens)

win_1 = pyglet.window.Window(screen=screens[0], fullscreen=True)
if n_screens>1:
    win_2 = pyglet.window.Window(screen=screens[1], fullscreen=True)
    win_3 = pyglet.window.Window(screen=screens[2], fullscreen=True)
else:
    print 'Running in single window mode '


# Parameters
# ----------
#scale = 2
#width, height = screen.width//scale,screen.height//scale
dt = 1.

# texture_uv holds U & V values (red and green channels)
# ------------------------------------------------------
image = np.ones((N_Y,N_X,4), dtype=np.float32)
#    image[:,:,0] = 1.0
#r = 4
#image[N_Y/2-r:N_Y/2+r, N_X/2-r:N_X/2+r, :] = 0.
#    image[height/2-r:height/2+r, width/2-r:width/2+r, 1] = 0.25
data = image.ctypes.data
texture_data = pyglet.image.Texture.create_for_size(
    gl.GL_TEXTURE_2D, N_X, N_Y, gl.GL_RGBA32F_ARB)
gl.glBindTexture(texture_data.target, texture_data.id)
gl.glTexParameteri(texture_data.target, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
gl.glTexParameteri(texture_data.target, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
gl.glTexImage2D(texture_data.target, texture_data.level, gl.GL_RGBA32F_ARB,
                N_X, N_Y, 0, gl.GL_RGBA, gl.GL_FLOAT, data)
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

@win_1.event
def on_draw():
    global particles, N, scenario
    gl.glClearColor(1.0,1.0,1.0,1.0)
    win_1.clear()

    particles = do_scenario(particles, scenario=scenario)

    data = image.ctypes.data

    gl.glTexImage2D(texture_data.target, texture_data.level, gl.GL_RGBA32F_ARB,
                    N_X, N_Y, 0, gl.GL_RGBA, gl.GL_FLOAT, data)
    gl.glViewport(0, 0, win_1.width, win_1.height)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(0, 1, 0, 1, -1, 1)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    color_shader.bind()

    texture_data.blit(x=0.0, y=0.0, width=1.0, height=1.0)


if n_screens>1:

    @win_2.event
    def on_draw():
        gl.glClearColor(1.0,1.0,1.0,1.0)
        win_2.clear()

        image = np.ones((height,width,4), dtype=np.float32)
        for i in range(N):
            image[np.trunc(particles[0, i]*height), np.trunc(particles[1, i]*width), :] = 0.

        data = image.ctypes.data
        gl.glTexImage2D(texture_data.target, texture_data.level, gl.GL_RGBA32F_ARB,
                        N_X, N_Y, 0, gl.GL_RGBA, gl.GL_FLOAT, data)
        gl.glViewport(0, 0, win_2.width, win_2.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, 1, 0, 1, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        color_shader.bind()

        texture_data.blit(x=0.0, y=0.0, width=1.0, height=1.0)


if n_screens>2:

    @win_3.event
    def on_draw():
        gl.glClearColor(1.0,1.0,1.0,1.0)
        win_3.clear()

        image = np.ones((height,width,4), dtype=np.float32)
        for i in range(N):
            image[np.floor(particles[0, i]*height), np.floor(particles[1, i]*width), :] = 0.

        data = image.ctypes.data

        gl.glTexImage2D(texture_data.target, texture_data.level, gl.GL_RGBA32F_ARB,
                        N_X, N_Y, 0, gl.GL_RGBA, gl.GL_FLOAT, data)
        gl.glViewport(0, 0, win_3.width, win_3.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, 1, 0, 1, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        color_shader.bind()

        texture_data.blit(x=0.0, y=0.0, width=1.0, height=1.0)



#pyglet.clock.schedule_interval(lambda dt: None, 1.0/60.0)
pyglet.clock.schedule(lambda dt: None)
win_1.set_visible(True)
pyglet.app.run()