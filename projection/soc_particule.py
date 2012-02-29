#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Particle-like simulations using pyglet

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
N_screen = 1 # uncomment to force display on one screen only
#N_screen = 2 # uncomment to force display on one screen only
if N_screen<len(screens): screens = screens[:N_screen]
# Parameters
# ----------
downscale = 2 # to debug
#downscale = 1 # the real stuff / beware the segmentation fault
# x, l’axe long, y l’axe transversal, z la hauteur
N_Y, N_Z = screen.width//downscale, screen.height//downscale # size of the simulation grid
# ---------
# Scenarios
# ---------
#scenario = 'calibration'
#scenario = 'calibration-grille'
scenario = 'rotating-circle'
#scenario = 'flock'
#scenario = 'navier-stokes'

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

N = 2048
#N = 1024
#N = 16
from scenarios import Scenario
s = Scenario(N, scenario)
#
#N = 1024 #nbre totale de points
##N = 4096
#
#particles = np.zeros((6, N), dtype=np.float32)
## x, l’axe long, y l’axe transversal, z la hauteur
#particles[0,:] = np.random.rand(N) * d_x
#particles[1,:] = np.random.rand(N) * d_y
#particles[2,:] = np.random.rand(N) * d_z
#particles[3:,:] = np.random.randn(3,N) * .01 # speed is measured in screen size per second
##particles[2,:] = particles[1,:]
##particles[3,:] = -particles[0,:]
global last_t
last_t = 1

global posx , posy , posz
posx=0
posy=0
posz=0

def read_sock():
    try :	
        Donnee, Client = sock.recvfrom (1024)
    except (KeyboardInterrupt):
        raise
    except:
        detect = 0
    else :
        #print"data =" ,Donnee 
	#Donnee = ((angle + x + y + "o")*nbr_player)+";"
	datasplit = Donnee.split(";")
	#print "datasplit =" , datasplit
	store_blob = [[ int(each2) for each2 in each.split(",") ] for each in datasplit]
	#print "ras"

	return store_blob

def read_pos():
    posx, posy = np.nan, np.nan
    try :
        a = read_sock()
    except:
        rien =0
    else:
        try:
            posx=a[0][0]
            posy=a[0][1]
        except:
            rien =0
        else:
            rien = 1
    return ((float(posx))/90.0) + 2.1, ((float(posy))/90.0) + 2.1


# Screen information
# ------------------
win_1 = pyglet.window.Window(screen=screens[0], fullscreen=True)
if N_screen>1: win_2 = pyglet.window.Window(screen=screens[1], fullscreen=True)
    if N_screen>2: win_3 = pyglet.window.Window(screen=screens[2], fullscreen=True)
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

switch_rgb = (scenario == 'calibration') or (scenario == 'calibration-grille')

win_1.set_visible(True)
@win_1.event
def on_draw():
    global s, i_scenario, t_last

    if switch_rgb: 
        gl.glColor3f(1.0, 0., 0.)
    else:
        gl.glColor3f(1.0, 1.0, 1.0)
    gl.glClearColor(1.0,1.0,1.0,1.0)
    win_1.clear()
    s.do_scenario()

    # pour juju: ici on capte les donnees et on les passe au scenario
    x, y = read_pos()
    if not(x==np.nan):
        s.center = np.array([x, y, d_z/2])

    data = s.projection(0).ctypes.data
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
        data = s.projection(1).ctypes.data
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
        data = s.projection(2).ctypes.data
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