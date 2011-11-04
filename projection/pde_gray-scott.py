#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright INRIA
# Contributors: Nicolas P. Rougier (Nicolas.Rougier@inria.fr)
#
# This software is governed by the CeCILL license under French law and abiding
# by the rules of distribution of free software. You can use, modify and/ or
# redistribute the software under the terms of the CeCILL license as circulated
# by CEA, CNRS and INRIA at the following URL
# http://www.cecill.info/index.en.html.
#
# As a counterpart to the access to the source code and rights to copy, modify
# and redistribute granted by the license, users are provided only with a
# limited warranty and the software's author, the holder of the economic
# rights, and the successive licensors have only limited liability.
#
# In this respect, the user's attention is drawn to the risks associated with
# loading, using, modifying and/or developing or reproducing the software by
# the user in light of its specific status of free software, that may mean that
# it is complicated to manipulate, and that also therefore means that it is
# reserved for developers and experienced professionals having in-depth
# computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling
# the security of their systems and/or data to be ensured and, more generally,
# to use and operate it in the same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.
# -----------------------------------------------------------------------------
"""
Reaction Diffusion : Gray-Scott model

References:
----------
Complex Patterns in a Simple System
John E. Pearson, Science 261, 5118, 189-192, 1993.

"""
import numpy as np
import glumpy
from solver import vel_step, dens_step, convolution_matrix
import os
############################################################################
HELP = ' Hi! wellcome to the wonderful world of gray-scott patterns! use the tab key to switch to and from fullscreen, the N key to change animal, C to change colormap, space to reset activities, H for this help, escape to exit '
############################################################################
screen_X, screen_Y = 1200, 1920
downscale = 10 # increase to match your CPU's speed
N_X, N_Y = screen_X/downscale, screen_Y/downscale # size of the simulation grid
############################################################################
# Parameters from http://www.aliensaint.com/uo/java/rd/
# -----------------------------------------------------
dt = 1.
dt_GS = 5e-1
N_GS = 5
t  = 10000
zoo = {'Pulses':        [0.16, 0.08, 0.020, 0.055],
       'Worms 0':       [0.16, 0.08, 0.050, 0.065], 
       'Worms 1':       [0.16, 0.08, 0.052, 0.065], 
       'Worms 2':       [0.16, 0.08, 0.054, 0.063],
       'Zebrafish':     [0.16, 0.08, 0.035, 0.060],
       'Bacteria 1':    [0.16, 0.08, 0.035, 0.065],
       'Bacteria 2':    [0.14, 0.06, 0.035, 0.065],
       'Coral':         [0.16, 0.08, 0.060, 0.062],
       'Fingerprint':   [0.19, 0.05, 0.060, 0.062],
       'Spirals':       [0.10, 0.10, 0.018, 0.050],
       'Spirals Dense': [0.12, 0.08, 0.020, 0.050],
       'Spirals Fast':  [0.10, 0.16, 0.020, 0.050],
       'Unstable':      [0.16, 0.08, 0.020, 0.055],
}
Ddens, Dinh, F, k = zoo['Spirals Dense']
diff = 0. # 1e-9
visc = 0. # 1e-12
force = .05
############################################################################
threshold, inc =.95, 1.01
cmaps = {'blue':glumpy.colormap.Colormap("blue",
                                 (0.00, (0.2, 0.2, 1.0)),
                                 (1.00, (1.0, 1.0, 1.0))),
        'grey':glumpy.colormap.Grey_r,
        'binary':glumpy.colormap.Colormap(
                                 (0.  , (1.,1.,1.,1.)),
                                 (threshold, (0.,0.,0.,1.)),
                                 (threshold*inc, (1.,1.,1.,1.)),
                                 (1.,   (1.,1.,1.,1.))),
        'binary_reversed':glumpy.colormap.Colormap(
                                 (0.  , (1.,1.,1.,1.)),
                                 (threshold, (1.,1.,1.,1.)),
                                 (threshold*inc, (0.,0.,0.,1.)),
                                 (1.,   (0.,0.,0.,1.))),
        'contours_reversed':glumpy.colormap.Colormap(
                                 (0.  , (1.,1.,1.,1.)),
                                 (threshold/inc, (1.,1.,1.,1.)),
                                 (threshold, (0.,0.,0.,1.)),
                                 (threshold*inc, (0.,0.,0.,1.)),
                                 (threshold*inc**2, (1.,1.,1.,1.)),
                                 (1.,   (1.,1.,1.,1.))),
        'contours':glumpy.colormap.Colormap(
                                 (0.  , (1.,1.,1.,1.)),
                                 (threshold/inc, (0.,0.,0.,1.)),
                                 (threshold, (1.,1.,1.,1.)),
                                 (threshold*inc, (1.,1.,1.,1.)),
                                 (threshold*inc**2, (0.,0.,0.,1.)),
                                 (1.,   (0.,0.,0.,1.)))
        }
cmap = cmaps['contours']
interpolation = 'bicubic'
# interpolation = 'nearest' # 
############################################################################
amp0, cycles = .05, 1
xx, yy = np.meshgrid(np.linspace(0, cycles*np.pi, N_Y), np.linspace(0, cycles*np.pi, N_X))
amp = 1 + amp0*(np.cos(xx)**2 + np.cos(yy)**2 )

# motion field
u     = np.zeros((N_X, N_Y), dtype=np.float32)
u_    = np.zeros((N_X, N_Y), dtype=np.float32)
v     = np.zeros((N_X, N_Y), dtype=np.float32)
v_    = np.zeros((N_X, N_Y), dtype=np.float32)
# chemicals
dens = np.zeros((N_X, N_Y), dtype = np.float32)
inh = np.zeros((N_X, N_Y), dtype = np.float32)
dens_ = np.zeros((N_X, N_Y), dtype = np.float32)
inh_ = np.zeros((N_X, N_Y), dtype = np.float32)
edge = np.zeros((N_X, N_Y), dtype = np.float32)
Z = dens_*inh_*inh_
K = convolution_matrix(Z,Z, np.array([[np.NaN,  1., np.NaN], 
                                      [  1.,   -4.,   1.  ],
                                      [np.NaN,  1., np.NaN]]))
Ldens = (K*dens_.ravel()).reshape(dens_.shape)
Linh = (K*inh_.ravel()).reshape(inh_.shape)

r = N_X / 5
dens[...] = 1.0
inh[...] = 0.0
dens[N_X/2-r:N_X/2+r,N_Y/2-r:N_Y/2+r] = 0.50
inh[N_X/2-r:N_X/2+r,N_Y/2-r:N_Y/2+r] = 0.25
dens += .05*np.random.random((N_X, N_Y))
inh += .05*np.random.random((N_X, N_Y))
dens_[...] = dens
inh_[...] = inh

amp0, cycles = .1, 1
xx, yy = np.meshgrid(np.linspace(0, cycles*np.pi, N_Y), np.linspace(0, cycles*np.pi, N_X))
amp = 1 + amp0*(np.cos(xx)**2 + np.cos(yy)**2)

fig = glumpy.figure((N_Y*downscale, N_X*downscale))
fig.last_drag = None
Zdens = glumpy.Image(dens, interpolation=interpolation, colormap=cmap)
t, t0, frames = 0, 0, 0

@fig.event
def on_key_press(key, modifiers):
    global Zdens, cmap, dens, inh, dens_, inh_, Z, Ddens, Dinh, F, k, N_X, N_Y
    if key == glumpy.window.key.TAB:
        if fig.window.get_fullscreen():
            fig.window.set_fullscreen(0)
        else:
            fig.window.set_fullscreen(1)
    elif key == glumpy.window.key.C:
        cmap_old=cmap
        while cmap_old==cmap:
            i = np.random.randint(0, len(cmaps.keys()))
            key = cmaps.keys()[i]
            cmap=cmaps[key]
        os.system('say colormap ' + key)
        Zdens = glumpy.Image(dens, interpolation=interpolation, colormap=cmap)
    elif key == glumpy.window.key.H:
        os.system('say ' + HELP)
    elif key == glumpy.window.key.B:
        os.system('say On two occasions, I have been asked by members of Parliament: "Pray, Mr. Babbage, if you put into the machine wrong figures, will the right answers come out?" I am not able to rightly apprehend the kind of confusion of ideas that could provoke such a question.  ')
    elif key == glumpy.window.key.N:
        i = np.random.randint(0, len(zoo.keys()))
        Ddens, Dinh, F, k = zoo.values()[i]
        os.system('say  switched parameters to  ' + zoo.keys()[i])
        print zoo.keys()[i]
    elif key == glumpy.window.key.SPACE:
        u[...] = u_[...] = 0.0
        v[...] = v_[...] = 0.0
    elif not(key == glumpy.window.key.ESCAPE):
        os.system('say wrong key, dude! ' + HELP)

@fig.event
def on_mouse_drag(x, y, dx, dy, button):
    fig.last_drag = x, y, dx, dy, button

@fig.event
def on_mouse_motion(x, y, dx, dy):
    fig.last_drag = x, y, dx, dy, 0

#@fig.event
#def on_mouse_drag(x, y, dx, dy, button):
#    global dens,inh,dens_,inh_,u, u_, v, v_, Z,Ddens,Dinh,F,k, N_X, N_Y
#    center =( int( (1-y/float(fig.height)) * (N_X-1)),
#              int( x/float(fig.width) * (N_Y-1)) )
#    if not button:
#        u_[center[0],center[1]] = -force * dy
#        v_[center[0],center[1]] = force * dx
#    else:
#        def distance(x,y):
#            return np.sqrt((x-center[0])**2+(y-center[1])**2)
#        D = np.fromfunction(distance,(N_X, N_Y))
#        M = np.where(D<=5,True,False).astype(np.float32)
#        dens_[...] = dens[...] = (1-M)*dens + M*0.50
#        inh_[...] = inh[...] = (1-M)*inh + M*0.25
#        Zdens.update()


@fig.event
def on_draw():
    fig.clear()
    Zdens.draw( x=0, y=0, z=0,
             width=fig.width, height=fig.height )

@fig.event
def on_idle(elapsed):
    global Zdens, dens,inh,dens_,inh_, u, u_, v, v_, Z, Ddens,Dinh,F,k, edge
    u_[...] = v_[...] = 0.0
#    dens_[...] = inh_[...] = 0.0

    if fig.last_drag:
        x, y, dx, dy, button = fig.last_drag
        center =( int( (1-y/float(fig.height)) * (N_X-1)),
                  int( x/float(fig.width) * (N_Y-1)) )
        if not button:
            u_[center[0],center[1]] = -force * dy
            v_[center[0],center[1]] = force * dx
        else:
            def distance(x,y):
                return np.sqrt((x-center[0])**2+(y-center[1])**2)
            D = np.fromfunction(distance,(N_X, N_Y))
            M = np.where(D<=5,True,False).astype(np.float32)
            dens_[...] = dens[...] = (1-M)*dens + M*0.50
            inh_[...] = inh[...] = (1-M)*inh + M*0.25
            Zdens.update()
        
    fig.last_drag = None

    # advection
    vel_step(N_X-2, N_Y-2, u, v, u_, v_, visc, dt)
    dens_step(N_X-2, N_Y-2, dens, 0.*dens_, u, v, diff, dt)
    dens_step(N_X-2, N_Y-2, inh, 0.*inh_, u, v, diff, dt)

    for i in range(N_GS):
        Ldens = (K*dens_.ravel()).reshape(dens_.shape)
        Linh = (K*inh_.ravel()).reshape(inh_.shape)
        dens += dt_GS * (Ddens*Ldens - Z +  amp*    F   *(1-dens_))
        inh += dt_GS * (Dinh*Linh + Z - (F+k)*inh_    )
        #dens_,inh_ = np.maximum(dens,0), np.maximum(inh,0)
        dens_,inh_ = dens, inh
        Z = dens_*inh_*inh_
        
#    Z = dens_*inh_*inh_
#    grad_mag, thinned_grad, edge = canny(dens)
    
    Zdens.update()
    fig.redraw()

    global t, t0, frames
    t += elapsed
    frames = frames + 1
    if t-t0 > 5.0:
        fps = float(frames)/(t-t0)
        print 'FPS: %.2f (%d frames in %.2f seconds)' % (fps, frames, t-t0)
        frames,t0 = 0, t

glumpy.show()
