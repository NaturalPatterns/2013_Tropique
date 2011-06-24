#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (C) 2011 _ Laurent Perrinet
"""
Gierer, A. and H. Meinhardt (1972), A theory of biological pattern formation. Kybernetik 12, 30-39.

"""
# Adapted from demo_smoke.py @ glumpy http://code.google.com/p/glumpy/source/browse/demos/demo-smoke.py?name=default
# Copyright (C) 2009-2010  Nicolas P. Rougier
#
# Distributed under the terms of the BSD License. The full license is in
# the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------
# Adapted from a post on comp.lang.python by Alberto Santini 
# Topic: Real-Time Fluid Dynamics for Games...
# Date: 02/20/05
# 
# Mouse click to add smoke
# Mouse move to add some turbulences
# -----------------------------------------------------------------------------
import sys
import numpy, glumpy
############################################################################
N = 128 # size of the simulation grid
size = N+2
dt = 0.02
downscale = 2
diff, diff_inh = 2.e-2, 1.e-2 #0., 0. #
rho_a, mu_a =  .0, 1.
rho_h, mu_h = .0, 1.

dens_noise, inh_noise = .1,  .1

steps=20
# visualization parameters
fullscreen = False # True #
interpolation= 'bicubic' # 'nearest' #
cmap = glumpy.colormap.Colormap("BlueGrey",
                                (0., (0.,0.,0.)), (1., (0.75,0.75,1.00)))
############################################################################
def set_bnd(N, b, x):
    """
    We assume that the fluid is contained in a box with solid walls: no flow
    should exit the walls. This simply means that the horizontal component of
    the velocity should be zero on the vertical walls, while the vertical
    component of the velocity should be zero on the horizontal walls. For the
    density and other fields considered in the code we simply assume
    continuity. The following code implements these conditions.
    """
    relax = 1.0
    if b == 1:
        x[0,:] = -relax *x[1,:]
        x[N+1,:] = -relax *x[N,:]
    else:
        x[0,:] = relax * x[1,:]
        x[N+1,:] = relax * x[N,:]
    if b == 2:
        x[:,0] = -relax *x[:,1]
        x[:,N+1] = -relax *x[:,N]
    else:
        x[:,0] = relax * x[:,1]
        x[:,N+1] = relax * x[:,N]
    x[0,0] = relax * 0.5*(x[1,0]+x[0,1])
    x[0,N+1] = relax * 0.5*(x[1,N+1]+x[0,N])
    x[N+1,0] = relax * 0.5*(x[N,0]+x[N+1,1])
    x[N+1,N+1] = relax * 0.5*(x[N,N+1]+x[N+1,N])



############################################################################
# initialization
u     = numpy.zeros((size,size), dtype=numpy.float32) # y velocity
u_    = numpy.zeros((size,size), dtype=numpy.float32)
v     = numpy.zeros((size,size), dtype=numpy.float32) # x velocity
v_    = numpy.zeros((size,size), dtype=numpy.float32)
dens  = numpy.zeros((size,size), dtype=numpy.float32) # density of activator
dens_ = numpy.zeros((size,size), dtype=numpy.float32)
inh  = numpy.zeros((size,size), dtype=numpy.float32) # density of inhibitor
inh_ = numpy.zeros((size,size), dtype=numpy.float32)
Z = numpy.zeros((N,N),dtype=numpy.float32)

x, y = numpy.mgrid[0:size,0:size]
x, y = x*1./(N+2), y*1./(N+2)
#f = size / 10.
#peigne = numpy.sin(y / f) ** 4

dens += dens_noise * numpy.random.randn(size,size)**2     
inh += inh_noise * numpy.random.randn(size,size)**2  

I = glumpy.Image(Z, interpolation=interpolation, cmap=cmap, vmin=0, vmax=1.)
t, t0, frames = 0,0,0

window = glumpy.Window(1600/downscale,900/downscale, fullscreen = fullscreen)
window.last_drag = None

# events
@window.event
def on_mouse_drag(x, y, dx, dy, button):
    window.last_drag = x,y,dx,dy,button

@window.event
def on_mouse_motion(x, y, dx, dy):
    window.last_drag = x,y,dx,dy,0

@window.event
def on_key_press(key, modifiers):
    global dens, dens_, inh, inh_, u, u_, v, v_, diff, diff_inh, rho_a, mu_a, rho_h, mu_h
    if key == glumpy.key.ESCAPE:
        sys.exit()
    elif key == glumpy.key.SPACE:
        dens[...] = dens_[...]= inh[...] = inh_[...]  = 0.0
        u[...] = u_[...] = 0.0
        v[...] = v_[...] = 0.0
    elif key == glumpy.key.T:
        diff *= 1.05
    elif key == glumpy.key.G:
        diff *= .95
    elif key == glumpy.key.Y:
        diff_inh *= 1.05
    elif key == glumpy.key.H:
        diff_inh *= .95
    elif key == glumpy.key.U:
        rho_a *= 1.05
    elif key == glumpy.key.J:
        rho_a *= .95
    elif key == glumpy.key.I:
        rho_h *= 1.05
    elif key == glumpy.key.K:
        rho_h *= .95
    elif key == glumpy.key.O:
        mu_a *= 1.05
    elif key == glumpy.key.L:
        mu_a *= .95
    elif key == glumpy.key.P:
        mu_h *= 1.05
    elif key == glumpy.key.M:
        mu_h *= .95
    print ' diff, diff_inh, rho_a, mu_a, rho_h, mu_h = ', diff, diff_inh, rho_a, mu_a, rho_h, mu_h


def lin_solve(N, b, x, x0, a, c, steps=20):
    for k in range(0, steps):
        x[1:N+1,1:N+1] = (x0[1:N+1,1:N+1]
                          +a*(x[0:N,1:N+1]  +
                              x[2:N+2,1:N+1]+
                              x[1:N+1,0:N]  +
                              x[1:N+1,2:N+2]))/c
        set_bnd(N, b, x)

def laplacian(N, b, x, x0):
    x[1:N+1,1:N+1] = -4 * x0[1:N+1,1:N+1] +(x0[0:N,1:N+1]   +
                                            x0[2:N+2,1:N+1] +
                                            x0[1:N+1,0:N]   +
                                            x0[1:N+1,2:N+2])
    set_bnd(N, b, x)

def diffuse(N, b, x, x0):
    x[1:N+1,1:N+1] = .5 * x0[1:N+1,1:N+1] + .125*(x0[0:N,1:N+1]   +
                                                x0[2:N+2,1:N+1] +
                                                x0[1:N+1,0:N]   +
                                                x0[1:N+1,2:N+2])
    set_bnd(N, b, x)

# main loop
@window.event
def on_idle(*args):
    global x, y, dens, dens_, inh, inh_, N, dt, diff, diff_inh, rho_a, mu_a, rho_h, mu_h
    window.clear()
    dens_[...] = inh_[...] = 0.0

#    print 'o' , dens.min(),  dens.max(), inh.min(),  inh.max()
#    lin_solve(N, 0, dens, dens_, diff, 1+4*diff)
##    print '>' , dens_.min(),  dens_.max(), inh.min(),  inh.max()
#    lin_solve(N, 0, inh, inh_, diff_inh, 1+4*diff_inh)
#    
#    # Heat equation
#    diffuse(N, 0, dens_, dens)
#    diffuse(N, 0, inh_, inh)
#    dens = (1-dt)*dens + dt * dens_
#    inh = (1-dt)*inh + dt *inh_ 


#    # Turing
    laplacian(N, 0, dens_, dens)
    laplacian(N, 0, inh_, inh)
    dens += rho_a* (16 - dens * inh) + diff * dens_ 
    inh += rho_h* (dens * inh - inh -12 - mu_h * y ) + diff_inh * inh_ 
#    modulation = .5 + .5 * tanh( inh)

#    dens = (1-dt)*dens + dt*( rho_a * (dens -  dens**3 + mu_a * x  - mu_h * inh) + diff * dens_ )
#    inh = (1-dt)*inh + dt*( rho_h * (dens  - inh) + diff_inh * inh_ )
#    
#    dens += dt*dens_noise *  numpy.random.randn(size,size)**2     
#    inh += dt*inh_noise * numpy.random.randn(size,size)**2  
#      

    print  dens.min(),  dens.max(), inh.min(),  inh.max()

#    dens = dens * (dens>0)
#    inh = inh * (inh>0)

#    Z[...] = dens_[0:-2,0:-2]
#    Z[...] = inh[0:-2,0:-2]
    Z[...] = .5 + .5 *numpy.tanh((dens[0:-2,0:-2]-dens.mean())/(dens.max()-dens.min()))
#    Z[...] = .5 + .5 *numpy.tanh(inh[0:-2,0:-2])
    I.update()
    I.blit(0,0,window.width,window.height)
    window.draw()

    global t, t0, frames
    t += args[0]
    frames = frames + 1
    if t-t0 > 5.0:
        fps = float(frames)/(t-t0)
        print 'FPS: %.2f (%d frames in %.2f seconds)' % (fps, frames, t-t0)
        frames,t0 = 0, t

window.mainloop()
