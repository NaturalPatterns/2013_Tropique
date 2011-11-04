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
dt = 0.01
visc = 0 #4.e-6
force = 0.5
source = 1.0
downscale = 4
diff, diff_inh = 2.e-5, 1.e-4 #0., 0. #
rho_a, mu_a =  1.1, 16.
rho_h, mu_h = .1, 12.5

dens_noise, inh_noise = 0.01,  0.01

steps=20
# visualization parameters
fullscreen = False # True #
interpolation= 'bicubic' # 'nearest' #
cmap = glumpy.colormap.Colormap("BlueGrey",
                                (0., (0.,0.,0.)), (1., (0.75,0.75,1.00)))
############################################################################
import scipy.weave as weave
from scipy.weave import converters
"""
Real-Time Fluid Dynamics for Games by Jos Stam (2003).
Parts of author's work are also protected
under U. S. patent #6,266,071 B1 [Patent].
"""

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


def lin_solve(N, b, x, x0, a, c, steps=steps):
    for k in range(0, steps):
        x[1:N+1,1:N+1] = (x0[1:N+1,1:N+1]
                          +a*(x[0:N,1:N+1]  +
                              x[2:N+2,1:N+1]+
                              x[1:N+1,0:N]  +
                              x[1:N+1,2:N+2]))/c
        set_bnd(N, b, x)

def laplacian(N, b, x, x0):
    x[1:N+1,1:N+1] = .25*(x0[0:N,1:N+1]   +
                          x0[2:N+2,1:N+1] +
                          x0[1:N+1,0:N]   +
                          x0[1:N+1,2:N+2])- x0[1:N+1,1:N+1]
    set_bnd(N, b, x)

# Addition of forces: the density increases due to sources
def add_source(N, x, s, dt):
    x += dt*s


# Diffusion: the density diffuses at a certain rate
def diffuse (N, b, x, x0, diff, dt):
    """
    The basic idea behind our method is to find the densities which when
    diffused backward in time yield the densities we started with.  The
    simplest iterative solver which works well in practice is Gauss-Seidel
    relaxation.
    """
    a = dt*diff*N*N
    lin_solve(N, b, x, x0, a, 1+4*abs(a))


# Advection: the density follows the velocity field
def advect (N, b, d, d0, u, v, dt):
    """
    The basic idea behind the advection step. Instead of moving the cell
    centers forward in time through the velocity field, we look for the
    particles which end up exactly at the cell centers by tracing backwards in
    time from the cell centers.
    """
    code = """
           #define MAX(a,b) ((a)<(b) ? (b) : (a))
           #define MIN(a,b) ((a)>(b) ? (b) : (a))

           float x, y, s1, s0, t1, t0;;
           int i0, i1, j0, j1;
           for (int i=1; i<(N+1); ++i) {
               for (int j=1; j<(N+1); ++j) {
                   x = MIN(MAX(i-dt0*u(i,j),0.5),N+0.5);
                   y = MIN(MAX(j-dt0*v(i,j),0.5),N+0.5);
                   i0 = int(x);
                   i1 = i0+1;
                   j0 = int(y);
                   j1 = j0+1;
                   s1 = x-i0;
                   s0 = 1-s1;
                   t1 = y-j0;
                   t0 = 1-t1;
                   d(i,j) = s0*(t0*d0(i0,j0)+t1*d0(i0,j1))+ 
                            s1*(t0*d0(i1,j0)+t1*d0(i1,j1));
                   }
               }
           #undef MIN
           #undef MAX
           """
    dt0 = dt*N
    # Does not work yet
    weave.inline(code, ['N', 'u', 'v', 'd', 'd0', 'dt0'],
                 type_converters=converters.blitz,
                 compiler='gcc')
    # for i in range(1, N+1):
    #     for j in range(1, N+1):
    #         x = min(max(i-dt0*u[i,j],0.5),N+0.5)
    #         y = min(max(j-dt0*v[i,j],0.5),N+0.5)
    #         i0 = int(x)
    #         i1 = i0+1
    #         j0 = int(y)
    #         j1 = j0+1
    #         s1 = x-i0
    #         s0 = 1-s1
    #         t1 = y-j0
    #         t0 = 1-t1
    #         d[i,j] = s0*(t0*d0[i0,j0]+t1*d0[i0,j1])+ \
    #                  s1*(t0*d0[i1,j0]+t1*d0[i1,j1])
    set_bnd (N, b, d)


def project(N, u, v, p, div):
    h = 1.0/N
    div[1:N+1,1:N+1] = -0.5*h*(u[2:N+2,1:N+1]
                               -u[0:N,1:N+1]
                               +v[1:N+1,2:N+2]
                               -v[1:N+1,0:N])
    p[1:N+1,1:N+1] = 0.
    set_bnd (N, 0, div)
    set_bnd (N, 0, p)
    lin_solve (N, 0, p, div, 1, 4)
    # ??? not in the paper /h
    u[1:N+1,1:N+1] -= 0.5*(p[2:N+2,1:N+1]-p[0:N,1:N+1])/h
    # ??? not in the paper /h
    v[1:N+1,1:N+1] -= 0.5*(p[1:N+1,2:N+2]-p[1:N+1,0:N])/h
    set_bnd (N, 1, u)
    set_bnd (N, 2, v)



# Evolving density: advection, diffusion, addition of sources
def dens_step (N, x, x0, u, v, diff, dt):
    add_source(N, x, x0, dt)
    x0, x = x, x0 # swap
    diffuse(N, 0, x, x0, diff, dt)
    x0, x = x, x0 # swap
    advect(N, 0, x, x0, u, v, dt)

# Evolving velocity: self-advection, viscous diffusion, addition of forces
def vel_step (N, u, v, u0, v0, visc, dt):
    add_source(N, u, u0, dt)
    add_source(N, v, v0, dt);
    u0, u = u, u0 # swap
    diffuse(N, 1, u, u0, visc, dt)
    v0, v = v, v0 # swap
    diffuse(N, 2, v, v0, visc, dt)
    project(N, u, v, u0, v0)
    u0, u = u, u0 # swap
    v0, v = v, v0 # swap
    advect(N, 1, u, u0, u0, v0, dt)
    advect(N, 2, v, v0, u0, v0, dt)
    project(N, u, v, u0, v0)
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
window = glumpy.Window((1600/downscale,900/downscale))#, fullscreen = fullscreen)
window.last_drag = None

dens += dens_noise * numpy.random.randn(size,size)**2     
inh += inh_noise * numpy.random.randn(size,size)**2  

I = glumpy.Image(Z, interpolation=interpolation, colormap=glumpy.colormap.Grey_r, vmin=0, vmax=1.)
t, t0, frames = 0,0,0

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



# main loop
@window.event
def on_idle(*args):
    global x, y, dens, dens_, inh, inh_, u, u_, v, v_, N, visc, dt, diff, diff_inh, rho_a, mu_a, rho_h, mu_h
    window.clear()
    dens_[...] = inh_[...] = u_[...] = v_[...] = 0.0
#    if window.last_drag:
#        x,y,dx,dy,button = window.last_drag
#        j = min(max(int((N+2)*x/float(window.width)),0),N+1)
#        i = min(max(int((N+2)*(window.height-y)/float(window.height)),0),N+1)
#        if not button:
#            u_[i,j] = -force * dy
#            v_[i,j] = force * dx
#        else:
##            dens_[i,j] = source
#            dens_[:,j] = source # creating a vertical line
#
    
    window.last_drag = None
#    vel_step(N, u, v, u_, v_, visc, dt)
#    dens_step(N, dens, dens_, u, v, 0, dt)
#    dens_step(N, inh, inh_, u, v, 0, dt)
    
#    meinhardt_step(N, dens, dens_, inh, inh_, u, v, diff, diff_inh, dt)
#    dens_step(N, dens, dens_, u, v, diff, dt)
#    dens_step(N, inh, inh_, u, v, diff_inh, dt)

#    inh += dt*( rho_h *  dens**2   - mu_h * inh)
#    dens += dt*(rho_a *  dens**2 /(1 + kappa_a * dens**2) / (1e-6 + inh) - mu_a * dens)
    
#    dens += dt* rho_a * numpy.tanh(dens**2 * inh  - mu_a*dens)
#    inh += dt* rho_h * numpy.tanh( 1. - mu_h* dens**2 * inh)

    # Turing
#    laplacian(N, 0, dens_, dens)
#    laplacian(N, 0, inh_, inh)

    dens_[1:N+1,1:N+1] = (dens[0:N,1:N+1]   +
                             dens[2:N+2,1:N+1] +
                             dens[1:N+1,0:N]   +
                             dens[1:N+1,2:N+2])- 4*dens[1:N+1,1:N+1]
    set_bnd(N, 0, dens_)

    inh_[1:N+1,1:N+1] = (inh[0:N,1:N+1]   +
                            inh[2:N+2,1:N+1] +
                            inh[1:N+1,0:N]   +
                            inh[1:N+1,2:N+2])- 4*inh[1:N+1,1:N+1]
    set_bnd(N, 0, inh_)

    dens = (1-dt)*dens + dt*(rho_a* (mu_a * x - dens * inh) + diff * dens_ )
    inh = (1-dt)*inh + dt*(rho_h* (dens * inh - inh - mu_h * y) + diff_inh * inh_ )
    
#    dens += dens_noise * x * numpy.random.randn(size,size)**2     
#    inh += inh_noise * y * numpy.random.randn(size,size)**2  
#      

    print  dens.min(),  dens.max(), inh.min(),  inh.max()
#    dens = .5 + .5 *numpy.tanh(dens/1.)
#    inh  = .5 + .5 *numpy.tanh(inh/1.)

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

glumpy.show()
