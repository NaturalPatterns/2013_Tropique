#!/usr/bin/env python
# ----------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions 
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------
# $Id:$

'''Demonstrates one way of fixing the display resolution to a certain
size, but rendering to the full screen.

The method used in this example is:

1. Set the OpenGL viewport to the fixed resolution
2. Render the scene using any OpenGL functions (here, just a polygon)
3. Copy the framebuffer into a texture
4. Reset the OpenGL viewport to the window (full screen) size
5. Blit the texture to the framebuffer

Recent video cards could also render the scene directly to the texture
using EXT_framebuffer_object.  (This is not demonstrated in this example).
'''
import sys
sys.path.append('..')

from pyglet.gl import *
import pyglet
from math import pi, sin, cos , sqrt
from pyglet.window import key
import socket 

from myclass import my_own_draw

platform = pyglet.window.get_platform()
display  = platform.get_default_display()
screens  = display.get_screens()
screen   = screens[0]

window = pyglet.window.Window(screen   = screens[0] , fullscreen =True)

# Create a fullscreen window using the user's desktop resolution.  You can
# also use this technique on ordinary resizable windows.
#window = pyglet.window.Window(fullscreen=True,resizable =True)

# Use 320x200 fixed resolution to make the effect completely obvious.  You
# can change this to a more reasonable value such as 800x600 here.
target_resolution = 1440, 900
#window = pyglet.window.Window(target_resolution)

global rx ,ry
rx , ry = 0,0

#def socket
UDP_IP=""
UDP_PORT=3003
sock = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP
sock.bind( (UDP_IP,UDP_PORT) )
#sock.settimeout(0)
sock.setblocking(0)

global posx , posy , posz, exposx , exposy, exposz
posx=1
posy=0
posz=0
exposx = 0
exposy = 0
exposz = 0

global scene 
scene = 0
global placex , placey
placex , placey = 0 , 0
global nbr_seg
nbr_seg =10
global witdh_line
witdh_line  = 1
global 	rmin, rmax
rmin = 50
rmax = 125  
global dx ,dy
dx ,dy = 10.0 , 10.0
global lateral
lateral = 0

global nbr_seg
nbr_seg = 25
global last_good
last_good=[]

global wavelist
wavelist=[]

def read_sock():
    try :	
        Donnee, Client = sock.recvfrom (1024)
    except (KeyboardInterrupt):
        raise
    except:
        detect = 0
    else :
        print"data =" ,Donnee 
	#Donnee = ((angle + x + y + "o")*nbr_player)+";"
	datasplit = Donnee.split(";")
	print "datasplit =" , datasplit
	store_blob = [ int(each2) for each2 in datasplit[0].split(" ") ]
	print "blob=" , store_blob

	return store_blob

from driver import FixedResolutionViewport
target_width, target_height = target_resolution
viewport = FixedResolutionViewport(window, 
    target_width, target_height, filtered=False)

# ---------
# Scenarios
# ---------
scenarios = ['calibration', 'calibration-grille', 'rotating-circle']#, 'flock', 'navier-stokes']
i_scenario = 2 #  scenario chosen

N = 2048
N = 1024
#N = 16
from scenarios import Scenario
s = Scenario(N, scenarios[i_scenario])



def createcircle ( k,  r , h) :
	glLineWidth (10	 )
	glBegin(GL_LINES)
	#glLineWidth (5 )
	for i in range (180):
		x = r * cos(i) -h
		y = r * sin(i) +h
		glVertex3f(x + k,y - h,0)
		
		x = r * cos(i + 0.1) - h
    		y = r * sin(i + 0.1) + k
    		glVertex3f(x + k, y - h,0)
	glEnd()
	glLineWidth (10	 )


class Gout(object):
    def __init__(self, xx = 0 , yy=0,vitvit = 1):
	self.x = xx
	self.y = yy
	self.vit = vitvit
	self.ray = 10
    def draw(self):
	createcircle(0,self.ray*4,0);
	createcircle(0,self.ray*2,0);
	createcircle(0,self.ray,0);
	self.ray += 0.05
	if (self.ray >= 200) : self.ray = 0.01 
	return self.ray
"""
class Afan(object):
    def __init__(self, xx = 0 , yy=0,vitvit = 1):
	self.x = xx
	self.y = yy
	self.vit = vitvit
	self.ray = 10
    def draw(self
"""

def draw_scene():
    global s, posx, posy, posz, exposy , exposx, exposz, a , last_good
    global nbr_seg, witdh_line , rmin, rmax,  dx,  dy , placex , placey , scene ,lateral
    global wavelist 
    try :
	a = read_sock()
    except:
	rien =0
    else:
	#print "a=",a
	try:
	    scene = a[0]
	    placex=a[1]
	    placey=a[2]
	    nbr_seg=a[3] + 1
	    witdh_line=a[4] +1
	    rmin = a[5]
	    rmax = a[6]
	    dx = a[7] + 0.001
	    dy = a[8] + 0.1
	    lateral = a[9]

	except:
	    rien =0
	else:
	    print "posx,posy" , posx,posy

    '''Draw the scene, assuming the fixed resolution viewport and projection
    have been set up.  This just draws the rotated polygon.'''
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()
    
    w, h = target_resolution
    glTranslatef(w/2, h/2, 0)
    glRotatef(0, 0, 0, 1)
    glColor3f(1, 1, 1)
    s = min(w, h) / 3
    #glRectf(-s, -s, s, s)
    """
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    glTranslatef(0, 0, -4)
    glRotatef(0, 0, 0, 1)
    glRotatef(0, 0, 1, 0)
    glRotatef(0, 1, 0, 0)
    """
    global rx,ry
    #print "rx =",rx, cos(rx)
    glOrtho(0,1,0,1,0,1)
    #glDisable(GL_LIGHTING)
    my_place = (cos(ry)+1) * 125
    diff = abs(my_place*2)
    my_own_draw(placex , placey , scene, lateral,  witdh_line,  nbr_seg ,rx ,ry,rmin ,rmax)
    #my_own_draw(my_place , -1 , diff)
    """
    if (int(ry) == 0 ) :
	print "ouais" , ry
	wavelist.append( Gout(0,0,10) )
    else : 
	print "nooon" , ry
    for onde in wavelist[:]:
	a= onde.draw()
	#print "aaaaaaa = ", a
	if (a >=1):  wavelist.remove(onde)
    """
    #gout.draw()

def update(dt):
    global rotate
    #rotate += dt * 20
    global rx, ry, rz , dx ,dy
    if (dt!=0): print "dt=",int (1/dt)
    rx += dt / dx
    rx %= 6.28
    ry += dt / dy
    ry %= 6.28

pyglet.clock.schedule_interval(update, 1/60.)

@window.event
def on_key_press(symbol, modifiers):
    print "passe par la", symbol ,modifiers
    if symbol == key.A:
        print 'The "A" key was pressed.'
	sys.exit(0)
    elif symbol == key.LEFT:
        print 'The left arrow key was pressed.'
    elif symbol == key.ENTER:
        print 'The enter key was pressed.'

@window.event
def on_draw():
    viewport.begin()
    window.clear()
    draw_scene()
    viewport.end()
    #gout.draw()

gout = Gout(25,250,10)
pyglet.app.run()
