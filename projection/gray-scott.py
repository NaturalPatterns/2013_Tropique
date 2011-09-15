#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright INRIA
# Contributors: Nicolas P. Rougier (Nicolas.Rougier@inria.fr)
#
# DANA is a computing framework for the simulation of distributed,
# asynchronous, numerical and adaptive models.
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
'''
Reaction Diffusion : Gray-Scott model

References:
----------
Complex Patterns in a Simple System
John E. Pearson, Science 261, 5118, 189-192, 1993.
'''
import numpy as np
import scipy.sparse as sp
import glumpy
from solver import vel_step, dens_step

############################################################################
screen_X, screen_Y = 1200, 1920
downscale = 10 # increase to match your CPU's speed
N_X, N_Y = screen_X/downscale, screen_Y/downscale # size of the simulation grid
############################################################################
# Parameters from http://www.aliensaint.com/uo/java/rd/
# -----------------------------------------------------
dt = 1.
dtGS = 1e-0
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
Ddens, Dinh, F, k = zoo['Worms 0']
diff = 0. # 1e-9
visc = 0. # 1e-12
force = .05
############################################################################
#cmap = glumpy.colormap.Colormap("blue",
#                                (0.00, (0.2, 0.2, 1.0)),
#                                (1.00, (1.0, 1.0, 1.0)))
cmap=glumpy.colormap.Grey_r
interpolation = 'bicubic' # 'nearest' #
N_do = 5
############################################################################
def convolution_matrix(src, dst, kernel, toric=True):
    '''
    Build a sparse convolution matrix M such that:

    (M*src.ravel()).reshape(src.shape) = convolve2d(src,kernel)

    You can specify whether convolution is toric or not and specify a different
    output shape. If output (dst) is different, convolution is only applied at
    corresponding normalized location within the src array.

    Building the matrix can be pretty long if your kernel is big but it can
    nonetheless saves you some time if you need to apply several convolution
    compared to fft convolution (no need to go to the Fourier domain).

    Parameters:
    -----------

    src : n-dimensional numpy array
        Source shape

    dst : n-dimensional numpy array
        Destination shape

    kernel : n-dimensional numpy array
        Kernel to be used for convolution

    Returns:
    --------

    A sparse convolution matrix

    Examples:
    ---------

    >>> Z = np.ones((3,3))
    >>> M = convolution_matrix(Z,Z,Z,True)
    >>> print (M*Z.ravel()).reshape(Z.shape)
    [[ 9.  9.  9.]
     [ 9.  9.  9.]
     [ 9.  9.  9.]]
    >>> M = convolution_matrix(Z,Z,Z,False)
    >>> print (M*Z.ravel()).reshape(Z.shape)
    [[ 4.  6.  4.]
     [ 6.  9.  6.]
     [ 4.  6.  4.]]
    '''

    # Get non NaN value from kernel and their indices.
    nz = (1 - np.isnan(kernel)).nonzero()
    data = kernel[nz].ravel()
    indices = [0,]*(len(kernel.shape)+1)
    indices[0] = np.array(nz)
    indices[0] += np.atleast_2d((np.array(src.shape)//2 - np.array(kernel.shape)//2)).T

    # Generate an array A for a given shape such that given an index tuple I,
    # we can translate into a flat index F = (I*A).sum()
    to_flat_index = np.ones((len(src.shape),1), dtype=int)
    if len(src.shape) > 1:
        to_flat_index[:-1] = src.shape[1]

    R, C, D = [], [], []
    dst_index = 0
    src_indices = []

    # Translate target tuple indices into source tuple indices taking care of
    # possible scaling (this is done by normalizing indices)
    for i in range(len(src.shape)):
        z = np.rint((np.linspace(0,1,dst.shape[i])*(src.shape[i]-1))).astype(int)
        src_indices.append(z)

    nd = [0,]*(len(kernel.shape))
    for index in np.ndindex(dst.shape):
        dims = []
        # Are we starting a new dimension ?
        if index[-1] == 0:
            for i in range(len(index)-1,0,-1):
                if index[i]: break
                dims.insert(0,i-1)
        dims.append(len(dst.shape)-1)
        for dim in dims:
            i = index[dim]

            if toric:
                z = (indices[dim][dim] - src.shape[dim]//2 +(kernel.shape[dim]+1)%2 + src_indices[dim][i]) % src.shape[dim]
            else:
                z = (indices[dim][dim] - src.shape[dim]//2 +(kernel.shape[dim]+1)%2 + src_indices[dim][i])
            n = np.where((z >= 0)*(z < src.shape[dim]))[0]
            if dim == 0:
                nd[dim] = n.copy()
            else:
                nd[dim] = nd[dim-1][n]
            indices[dim+1] = np.take(indices[dim], n, 1)
            indices[dim+1][dim] = z[n]
        dim = len(dst.shape)-1
        z = indices[dim+1]
        R.extend( [dst_index,]*len(z[0]) )
        C.extend( (z*to_flat_index).sum(0).tolist() )
        D.extend( data[nd[-1]].tolist() )
        dst_index += 1

    return sp.coo_matrix( (D,(R,C)), (dst.size,src.size)).tocsr()

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
Z = dens_*inh_*inh_
K = convolution_matrix(Z,Z, np.array([[np.NaN,  1., np.NaN], 
                                      [  1.,   -4.,   1.  ],
                                      [np.NaN,  1., np.NaN]]))
Ldens = (K*dens_.ravel()).reshape(dens_.shape)
Linh = (K*inh_.ravel()).reshape(inh_.shape)

r = N_X / 20
dens[...] = 1.0
inh[...] = 0.0
dens[N_X/2-r:N_X/2+r,N_Y/2-r:N_Y/2+r] = 0.50
inh[N_X/2-r:N_X/2+r,N_Y/2-r:N_Y/2+r] = 0.25
dens += .05*np.random.random((N_X, N_Y))
inh += .05*np.random.random((N_X, N_Y))
dens_[...] = dens
inh_[...] = inh

fig = glumpy.figure((N_Y*downscale, N_X*downscale)) # , fullscreen = fullscreen
fig.last_drag = None
Zdens = glumpy.Image(dens, interpolation=interpolation, colormap=cmap)
t, t0, frames = 0,0,0

@fig.event
def on_key_press(key, modifiers):
    global dens,inh,dens_,inh_,Z,Ddens,Dinh,F,k, N_X, N_Y
    if key == glumpy.window.key.N:
        i = np.random.randint(0, len(zoo.keys()))
        Ddens, Dinh, F, k = zoo.values()[i]
        print zoo.keys()[i]
    elif key == glumpy.window.key.SPACE:
        u[...] = u_[...] = 0.0
        v[...] = v_[...] = 0.0


@fig.event
def on_mouse_drag(x, y, dx, dy, button):
    fig.last_drag = x,y,dx,dy,button

@fig.event
def on_mouse_motion(x, y, dx, dy):
    fig.last_drag = x,y,dx,dy,0

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
    global dens,inh,dens_,inh_, u, u_, v, v_, Z,Ddens,Dinh,F,k
    u_[...] = v_[...] = 0.0
#    dens_[...] = inh_[...] = 0.0

    if fig.last_drag:
        x,y,dx,dy,button = fig.last_drag
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


    for i in range(N_do):
        Ldens = (K*dens_.ravel()).reshape(dens_.shape)
        Linh = (K*inh_.ravel()).reshape(inh_.shape)
        dens += dtGS * (Ddens*Ldens - Z +  F   *(1-dens_))
        inh += dtGS * (Dinh*Linh + Z - (F+k)*inh_    )
        #dens_,inh_ = np.maximum(dens,0), np.maximum(inh,0)
        dens_,inh_ = dens, inh
        Z = dens_*inh_*inh_
        
    Z = dens_*inh_*inh_
    Zdens.update()
    fig.draw()

    global t, t0, frames
    t += elapsed
    frames = frames + 1
    if t-t0 > 5.0:
        fps = float(frames)/(t-t0)
        print 'FPS: %.2f (%d frames in %.2f seconds)' % (fps, frames, t-t0)
        frames,t0 = 0, t

glumpy.show()
