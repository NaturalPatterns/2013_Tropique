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
#pyglet.options['debug_gl'] = False
import pyglet.gl as gl
from shader import Shader
platform = pyglet.window.get_platform()
display  = platform.get_default_display()
screens  = display.get_screens()
screen   = screens[0]
# Parameters
# ----------
downscale = 4 # to debug
#downscale = 1 # the real stuff
# x, l’axe long, y l’axe transversal, z la hauteur
N_Y, N_Z = screen.width//downscale, screen.height//downscale # size of the simulation grid
# Projection information
# ----------------------
# taille du plan de reference
d_y, d_z = 7., 7.*N_Z/N_Y # en metres
# distance du plan de reference
d_x = 8. # en metres
# position spatiale des VPs par rapport au centre du plan de reference
x_VPs = [ d_x, d_x, d_x ] # en metres; placement regulier en profondeur a equidistance du plan de ref (le long d'un mur)
y_VPs = [ .5*d_y, .3*d_y, .7*d_y ] # en metres; placement regulier, le centre en premier
z_VPs = [ d_z/2, d_z/2, d_z/2] # en metres; on a place les VPs a la hauteur du centre du plan de reference
# ---------
# Scenarios
# ---------
scenario = 'calibration'
#scenario = 'flock'
#scenario = 'navier-stokes'

N = 1024
#N = 16
particles = np.zeros((6, N), dtype=np.float32)
# x, l’axe long, y l’axe transversal, z la hauteur
particles[0,:] = np.random.rand(N) * d_x
particles[1,:] = np.random.rand(N) * d_y
particles[2,:] = np.random.rand(N) * d_z
particles[3:,:] = np.random.randn(3,N) * .01 # speed is measured in screen size per second
#particles[2,:] = particles[1,:]
#particles[3,:] = -particles[0,:]
def do_scenario(particles, scenario):
    global t
    t_last = t
    t = time.time()  
    if scenario == 'calibration':
        particles[0,:], particles[1,:], particles[2,:] = 0., d_y/2, d_z/2
        frequency = .1 # how fast the whole disk moves in Hz
        radius = .3 * d_z
        N_dots = 16
        angle = 2 * np.pi *  frequency *  t + np.linspace(0, 2 * np.pi, N_dots)
        # a circle on the reference plane
        particles[0,:N_dots] = 0. # on the refrerence plane
        particles[1,:N_dots] = d_y/2 + radius * np.sin(angle)
        particles[2,:N_dots] = d_z/2 + radius * np.cos(angle)
        # a circle in front going opposite sign
        particles[0,N_dots:2*N_dots] = 1. # on the refrerence plane
        particles[1,N_dots:2*N_dots] = d_y/2 + radius * np.sin(-angle)
        particles[2,N_dots:2*N_dots] = d_z/2 + radius * np.cos(-angle)

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


#    particles[0,:] = np.mod(particles[0,:], N_X)
#    particles[1,:] = np.mod(particles[1,:], N_Y)
    
    return particles


def projection(particles, i_VP, xc=0, yc=0., zc=0.): # yc=d_y/2., zc=d_z/2.):#
    # (xc, yc, zc) = coordonnees en metres du point (a gauche, en bas) du plan de reference

    # TODO remove particles that are outside the depth range

    # convert the position of each particle to a el, az coordinate projected on the reference plane
    x, y, z = particles[0,:], particles[1,:], particles[2,:]
    az = ((yc-y)*(xc-x_VPs[i_VP])-(yc-y_VPs[i_VP])*(xc-x))/(x_VPs[i_VP]-x)
    el = ((zc-z)*(xc-x_VPs[i_VP])-(zc-z_VPs[i_VP])*(xc-x))/(x_VPs[i_VP]-x)
#    # remove those that are outside the VP range
#    az = az[0 < az < d_y]
#    el = el[0 < el < d_z]
    # convert to integers
    az, el = np.floor(az*N_Y/d_y), np.floor(el*N_Z/d_z)
    image = np.ones((N_Z,N_Y,4), dtype=np.float32)
    for i in range(N):
        if (0 <  az[i] < N_Y) and (0 < el[i] < N_Z):
            image[el[i], az[i], :] = 0.
    return image

# Screen information
# ------------------
n_screens = len(screens)
win_1 = pyglet.window.Window(screen=screens[0], fullscreen=True)
if n_screens>1:
    win_2 = pyglet.window.Window(screen=screens[1], fullscreen=True)
    win_3 = pyglet.window.Window(screen=screens[2], fullscreen=True)
else:
    print 'Running in single window mode '

dt = 1.

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

@win_1.event
def on_draw():
    global particles, N, scenario
    gl.glClearColor(1.0,1.0,1.0,1.0)
    win_1.clear()
    particles = do_scenario(particles, scenario=scenario)
    data = projection(particles, 0).ctypes.data
    gl.glTexImage2D(texture_data.target, texture_data.level, gl.GL_RGBA32F_ARB,
                    N_Y, N_Z, 0, gl.GL_RGBA, gl.GL_FLOAT, data)
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
        data = projection(particles, 1).ctypes.data
        gl.glTexImage2D(texture_data.target, texture_data.level, gl.GL_RGBA32F_ARB,
                        N_Y, N_Z, 0, gl.GL_RGBA, gl.GL_FLOAT, data)
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
        data = projection(particles, 2).ctypes.data
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
win_1.set_visible(True)
pyglet.app.run()