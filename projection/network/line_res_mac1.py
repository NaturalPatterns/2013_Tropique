#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Particle-like simulations using pyglet and a ugly bitmat
@author: BIOGENE&lolo

"""
DEBUG = False
import sys
sys.path.append('..')

# Screen information
# ------------------
from parametres import VPs, p, volume, run_thread_network_config

from network import VP
vps= VP(run_thread_network_config['ip_to_line_res'] , 7005 , 7006)
pdata = VP("10.42.0.1" , 9005 , 9006)

import numpy as np

import socket
import fcntl
import struct

from fanclass import my_own_draw #, createline
global rx ,ry
rx = 1
ry = 1
global dx ,dy
dx ,dy = 10.0 , 10.0

#def get_ip_address(ifname):
#    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    return socket.inet_ntoa(fcntl.ioctl(
#        s.fileno(),
#        0x8915,  # SIOCGIFADDR
#        struct.pack('256s', ifname[:15])
#    )[20:24])
#my_ip = get_ip_address('eth0')

my_ip = "10.42.0.51"
print "my ip is =", my_ip


global my_x ,my_y,my_z, my_cx,my_cy,my_cz,my_foc,my_pc_min,my_pc_max
        
for i in range (3):
    print VPs[i]['address']
    if (my_ip == VPs[i]['address']) :
        i_win= i
        print 'found my preset'
        my_x = VPs[i]['x']
        my_y= VPs[i]['y']
        my_z= VPs[i]['z']
        my_cx= VPs[i]['cx']
        my_cy= VPs[i]['cy']
        my_cz= VPs[i]['cz']
        my_foc= VPs[i]['foc']
        my_pc_min= VPs[i]['pc_min']
        my_pc_max= VPs[i]['pc_max']




import pyglet
platform = pyglet.window.get_platform()
print "platform" , platform
display = platform.get_default_display()
print "display" , display
screens = display.get_screens()
print "screens" , screens
for i, screen in enumerate(screens):
    print 'Screen %d: %dx%d at (%d,%d)' % (i, screen.width, screen.height, screen.x, screen.y)
N_screen = len(screens) # number of screens
assert N_screen == 1 # we should be running on one screen only

from pyglet.window import Window
win_0 = Window(screen=screens[0], fullscreen=True, resizable=True, vsync = True)
win_0.set_exclusive_mouse()
import pyglet.gl as gl
from pyglet.gl.glu import gluLookAt

def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    gl.glEnable(gl.GL_BLEND)
    gl.glShadeModel(gl.GL_SMOOTH)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_DONT_CARE)# gl.GL_NICEST)#
    gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glDisable(gl.GL_LINE_SMOOTH)
    gl.glColor3f(1.0, 1.0, 1.0)

win_0.on_resize = on_resize
win_0.set_visible(True)
win_0.set_mouse_visible(False)
gl.glMatrixMode(gl.GL_MODELVIEW)
gl.glLoadIdentity()
gl.gluPerspective(my_foc, 1.0*win_0.width/win_0.height, my_pc_min, my_pc_max)
gluLookAt(my_x, my_y, my_z,my_cx, my_cy, my_cz,0., 0, 1.0)
gl.glEnable(gl.GL_LINE_STIPPLE)

#      
d_x, d_y, d_z = volume
#import numpy as np
center = np.array([0., d_y/2, d_z/2], dtype='f') # central point of the room  / pont focal, pour lequel on optimise kinect et VPs?
#roger = np.array([d_x/2, d_y/2, d_z/2], dtype='f') #  fixation dot  (AKA Roger?)
#origin = np.array([0., 0., 0.], dtype='f') # origin

#VPs = VPs
N = p['N']
#print " the N= ", N

order = 2
particles = np.zeros((6*order, N), dtype='f') # x, y, z, u, v, w
##         self.particles[0:6, :] = np.random.randn(6, self.N)*d_y/4
particles[0:3, :] += center[:, np.newaxis]+ np.random.randn(3, N)*d_y/16
particles[3:6, :] += center[:, np.newaxis] + np.random.randn(3, N)*d_y/16
#
my_part = particles[0:6, :]
#offset = np.zeros((6*order, N), dtype='f') + np.array([0.3, 0., 0., 0.3, 0., 0.])[:, np.newaxis]
global placex , placey , scene, lateral,  witdh_line,  nbr_seg ,rx ,ry,rmin ,rmax , my_color
scene = 0
placex , placey = 0 , 0
witdh_line  = 1
rmin =2
rmax = 12  
dx ,dy = 10.0 , 10.0
lateral = 0
nbr_seg = 12
my_color=0
@win_0.event
def on_draw():
    global rx, ry, rz , dx ,dy
    global my_part, offset
    win_0.clear()
    
    gl.glLineWidth (p['line_width'])
    gl.glColor3f(1-my_color,1-my_color,1-my_color)
#    gl.glMatrixMode(gl.GL_MODELVIEW)
#    gl.glLoadIdentity()
#    gl.gluPerspective(VPs[0]['foc'], 1.0*win_0.width/win_0.height,
#                      VPs[0]['pc_min'], VPs[0]['pc_max'])
#    gluLookAt(VPs[0]['x'], VPs[0]['y'], VPs[0]['z'],
#          VPs[0]['cx'], VPs[0]['cy'], VPs[0]['cz'], 0., 0, 1.0)


    gl.glLineWidth ( 1 )
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    gl.gluPerspective(my_foc, 1.0*win_0.width/win_0.height, my_pc_min, my_pc_max)
    gluLookAt(my_x, my_y, my_z,my_cx, my_cy, my_cz,0., 0, 1.0)
    
    global s, vps, N
    try : 
        vps.trigger()
    except :
        pass
#    vps.trigger()
    particlestest = vps.listen()
     
    if (particlestest!=None):
        #print 'ok dude',  particlestest.shape
        my_part = np.fromstring(particlestest, dtype='f')
        
    gl.glLineWidth ( p['line_width'] )
    
    pyglet.graphics.draw(2*N, gl.GL_LINES, ('v3f', my_part.T.ravel().tolist()))
#    pyglet.graphics.draw(2*N, gl.GL_LINES, ('v3f', (my_part+offset).T.ravel().tolist()))
#    pyglet.graphics.draw(2*N, gl.GL_LINES, ('v3f', (my_part + np.array([0.3, 0., 0., 0.3, 0., 0.])[:, np.newaxis]).T.ravel().tolist()))
#    pyglet.graphics.draw(2*N, gl.GL_LINES, ('v3f', my_part.tolist()))
    print my_part.shape #(my_part + np.array([0.3, 0., 0., 0.3, 0., 0.])[:, np.newaxis]).T.shape
#    pyglet.graphics.draw(2*N, gl.GL_LINES, ('v3f', (my_part + np.array([0.3, 0., 0., 0.3, 0., 0.])).tolist()))
#    gl.glLineStipple (1, 0x0101)  # dotted
#    gl.glLineStipple (1, 0x0101)  # dotted
#    gl.glLineStipple (2, 0x00FF)  # dashed
#    gl.glLineStipple(1, 0x5555)
    
    global placex , placey , scene, lateral,  witdh_line,  nbr_seg ,rx ,ry,rmin ,rmax,my_color
    pdata.trigger()
    try : 
        data_fan = pdata.listen()
    except :
        pass
    else :
            if (data_fan!=None):
                datasplit = data_fan.split(";")
                store_blob = [int(each2) for each2 in datasplit[0].split(" ") ]
                scene = store_blob[0]
                placex , placey = float(store_blob[1]/100.0), float (store_blob[2]/100.0)
                nbr_seg = store_blob[3]
                witdh_line  = store_blob[4]
                rmin = store_blob[5]/50.0
                rmax = store_blob[6]/50.0
                dx= store_blob[7]/2
                my_color = store_blob[10]/255.0
                
    gl.glColor3f(my_color, my_color , my_color)
    
#    my_own_draw(placex , placey , scene, lateral,  witdh_line,  nbr_seg ,rx ,ry,rmin ,rmax)


    
def callback(dt):
    global rx, ry, rz , dx ,dy
    #if (dt!=0): print "dt=",int (1/dt)
    rx += dt / (dx+1)
    rx %= 6.28
    ry += dt / dy
    ry %= 6.28
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
