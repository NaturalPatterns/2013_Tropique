#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (C) 2011 _ Laurent Perrinet
"""

Turing 52 implementation using scipy's Laplace function.


@article{Turing52,
	Author = {Turing, A.},
	Comment = {A. M. Turing (1952). The Chemical Basis of Morphogenesis. Philosophical Transactions of the Royal Society of London, volume B 237, pages 37--72. [turing:1952] A. M. Turing (1992). The morphogen theory of phyllotaxis. In Saunders (1992). [turing:1992] A. N. Kolmogorov and I. G. Petrovsky and N. S. Piskunov (1937). Etude de l'{\'e}quation de la diffusion avec croissance de la quantit{\'e} de mati{\'e}re et son application {\`a} un probl{\'e}me biologique. Bulletin Universit{\'e} d'Etat {\`a} Moscou (Bjul. Moskowskogo Gos. Univ.), S{\'e}rie Internationale, volume Section A 1, pages 1-26. [kpp:1937] [Actually, I've never checked this reference or looked at it. Presumably it introduces the KPP equation I learnt about as a graduate student, in which case I'm not sure it was quite as long unknown as my quote from Jean implies]. (in http://www.swintons.net/deodands/references.html )},
	Journal = {Philosophical {T}ransactions of the {R}oyal {S}ociety of {L}ondon},
	Title = {The chemical basis of morphogenesis},
	Volume = {B},
	Year = {1952},
}


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
import numpy, glumpy
from scipy.ndimage.filters import laplace
############################################################################
screen_X, screen_Y = 1200, 1920
downscale = 10 # increase to match your CPU's speed
N_X, N_Y = screen_X/downscale, screen_Y/downscale # size of the simulation grid
############################################################################
dt = 0.02
# http://www.cs.utah.edu/~gk/papers/tvcg00/node7.html 
#/ http://www-inrev.univ-paris8.fr/extras/Michel-Bret/cours/bret/cours/math/st.htm
diff, diff_inh = .25, .0625 #0., 0. #
rho_a, mu_a =  .03125, 16.
rho_h, mu_h = .03125, 12.
init = 4.
dens_noise, inh_noise = .05,  .05
############################################################################
# visualization parameters
N_do = 5
interpolation= 'bicubic' # 'nearest' #
# TODO : show both populations
cmap = glumpy.colormap.Colormap("BlueGrey",
                                (0., (0.,0.,0.)), (1., (0.75,0.75,1.00)))
############################################################################
# initialization
dens  = init * numpy.ones((N_X, N_Y), dtype=numpy.float32) # density of activator
inh  = init * numpy.ones((N_X, N_Y), dtype=numpy.float32) # density of inhibitor
dens += dens_noise * numpy.random.randn(N_X, N_Y)**2     
inh += inh_noise * numpy.random.randn(N_X, N_Y)**2  
fig = glumpy.figure((N_Y*downscale, N_X*downscale)) # , fullscreen = fullscreen
Zu = glumpy.Image(dens, interpolation=interpolation, colormap=cmap)
############################################################################
@fig.event
def on_key_press(key, modifiers):
    global dens, inh, dens_noise, inh_noise, N_X, N_Y
    if key == glumpy.window.key.N:
        dens = init + dens_noise * numpy.random.randn(N_X, N_Y)**2     
        inh = init + inh_noise * numpy.random.randn(N_X, N_Y)**2  

@fig.event
def on_mouse_drag(x, y, dx, dy, button):
    global dens, inh, dens_noise, inh_noise, N_X, N_Y
    center =( int( (1-y/float(fig.height)) * (N_X-1)),
              int( x/float(fig.width) * (N_Y-1)) )
    def distance(x,y):
        return numpy.sqrt((x-center[0])**2+(y-center[1])**2)
    D = numpy.fromfunction(distance,(N_X, N_Y))
    M = numpy.where(D<=5,True,False).astype(numpy.float32)
    dens[...] = (1-M)*dens + M*init
#    inh[...] = (1-M)*inh + M*0.25
    Zu.update()

@fig.event
def on_draw():
    fig.clear()
    Zu.draw( x=0, y=0, z=0,
             width=fig.width, height=fig.height )

@fig.event
def on_idle(elasped):
    global dens, inh, dens_noise, inh_noise, N_X, N_Y
    for i in range(N_do):
        # Heat equation
        #    dens +=  diff * laplace(dens, mode='wrap')
    
        # Turing    
        dens += (rho_a * (mu_a - dens * inh) + diff * laplace(dens, mode='wrap'))*dt
        inh += (rho_h * (dens * inh - inh - mu_h + inh_noise * numpy.random.randn(N_X, N_Y) ) + diff_inh * laplace(inh, mode='wrap'))*dt    
    
        # Fitzhugh-Nagumo
        #    dens += (rho_a * (mu_a - dens * inh) + diff * laplace(dens, mode='wrap'))*dt
        #    inh += (rho_h * (dens * inh - inh - mu_h + inh_noise * numpy.random.randn(N,N) ) + diff_inh * laplace(inh, mode='wrap'))*dt
        
    Zu.update()
    fig.draw()

glumpy.show()