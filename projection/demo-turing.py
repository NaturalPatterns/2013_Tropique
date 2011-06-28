#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (C) 2011 _ Laurent Perrinet
"""

Turing 52 implementation + guests


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
import sys
import numpy, glumpy
from scipy.ndimage.filters import laplace
############################################################################
N = 128 # size of the simulation grid
reaction_type = 'Turing' # 'GrayScott' # 

if reaction_type == 'Turing':
    dt = 0.02
    # http://www.cs.utah.edu/~gk/papers/tvcg00/node7.html 
    #/ http://www-inrev.univ-paris8.fr/extras/Michel-Bret/cours/bret/cours/math/st.htm
    diff, diff_inh = .25, .0625 #0., 0. #
    rho_a, mu_a =  .03125, 16.
    rho_h, mu_h = .03125, 12.
    init = 4.
    source = init
elif reaction_type == 'GrayScott':
    dt = 1e-0
    diff, diff_inh = 2e-5, 1e-5 #0., 0. #
#    F, k = 0.098, 0.057 # (persistent stripes that form a linked network of polygonal cells, with gradual evolution into fewer and larger cells reminiscent of soap bubbles)
#    F, k = 0.014, 0.057 # showed briefly while looking for a better example)
    F, k = 0.014, 0.055 #(low-U high-V spots that move a bit, then "split" into two spots which then move and split again, etc.)
    # skate    
    F, k = 0.0620, 0.0609
#    F, k = 0.06, 0.0620 # F=0.0260, k=0.0530.
    init = 0.
    source =.5


dens_noise, inh_noise = .05,  .05

# visualization parameters
downscale = 2
fullscreen = False # True #
interpolation= 'bicubic' # 'nearest' #
# TODO : show both populations
cmap = glumpy.colormap.Colormap("BlueGrey",
                                (0., (0.,0.,0.)), (1., (0.75,0.75,1.00)))
############################################################################

############################################################################
# initialization
dens  = init * numpy.ones((N,N), dtype=numpy.float32) # density of activator
inh  = init * numpy.ones((N,N), dtype=numpy.float32) # density of inhibitor
dens += dens_noise * numpy.random.randn(N,N)**2     
inh += inh_noise * numpy.random.randn(N,N)**2  

Z = numpy.zeros((N,N),dtype=numpy.float32)
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
    global dens, inh, dens_noise, inh_noise, dt, diff, diff_inh, rho_a, mu_a, rho_h, mu_h
    if key == glumpy.key.ESCAPE:
        sys.exit()
    elif key == glumpy.key.SPACE:
#        dens[...] = inh[...]  = 0.0
        dens = dens_noise * numpy.random.randn(N,N)**2     
        inh = inh_noise * numpy.random.randn(N,N)**2  

#    elif key == glumpy.key.R:
#        dt *= 1.0125
#    elif key == glumpy.key.D:
#        dt *= .9875
#    elif key == glumpy.key.T:
#        diff *= 1.0125
#    elif key == glumpy.key.F:
#        diff *= .9875
#    elif key == glumpy.key.Y:
#        diff_inh *= 1.0125
#    elif key == glumpy.key.G:
#        diff_inh *= .9875
#    elif key == glumpy.key.U:
#        rho_a *= 1.0125
#    elif key == glumpy.key.H:
#        rho_a *= .9875
#    elif key == glumpy.key.I:
#        rho_h *= 1.0125
#    elif key == glumpy.key.J:
#        rho_h *= .9875
#    elif key == glumpy.key.O:
#        mu_a *= 1.0125
#    elif key == glumpy.key.K:
#        mu_a *= .9875
#    elif key == glumpy.key.P:
#        mu_h *= 1.0125
#    elif key == glumpy.key.L:
#        mu_h *= .9875
#    print ' dt, diff, diff_inh, rho_a, rho_h, mu_a, mu_h = ', dt, diff, diff_inh, rho_a, rho_h, mu_a, mu_h
#

# main loop
@window.event
def on_idle(*args):
    global dens, inh, dens_noise, inh_noise, dt, diff, diff_inh, rho_a, mu_a, rho_h, mu_h
    window.clear()
    if window.last_drag:
        x,y,dx,dy,button = window.last_drag
        j = min(max(int(N*x/float(window.width)),0),N-1)
        i = min(max(int(N*(window.height-y)/float(window.height)),0),N-1)
        if  button:#False:#not button:
#            u_[i,j] = -force * dy
#            v_[i,j] = force * dx
#        else:
#            print i,j
            dens[i,j] = inh[i,j] = source
#            dens_[:,j] = source # creating a vertical line
    
    window.last_drag = None
    
    # Heat equation
#    dens +=  diff * laplace(dens, mode='wrap')
    if reaction_type == 'Turing':

        # Turing    
        dens += (rho_a * (mu_a - dens * inh) + diff * laplace(dens, mode='wrap'))*dt
        inh += (rho_h * (dens * inh - inh - mu_h + inh_noise * numpy.random.randn(N,N) ) + diff_inh * laplace(inh, mode='wrap'))*dt

    elif reaction_type == 'GrayScott':
        #  Gray-Scott model : http://mrob.com/pub/comp/xmorphia/
        dens += (- dens * inh**2 + F * (1. - dens) + diff * laplace(dens, mode='wrap'))*dt
        inh += ( dens * inh**2 - (F + k) * inh  + diff_inh * laplace(inh, mode='wrap'))*dt    

    # Fitzhugh-Nagumo
#    dens += (rho_a * (mu_a - dens * inh) + diff * laplace(dens, mode='wrap'))*dt
#    inh += (rho_h * (dens * inh - inh - mu_h + inh_noise * numpy.random.randn(N,N) ) + diff_inh * laplace(inh, mode='wrap'))*dt
    


    Z[...] = (dens-dens.min())/(dens.max()-dens.min())
    I.update()
    I.blit(0,0,window.width,window.height)
    window.draw()

    global t, t0, frames
    t += args[0]
    frames = frames + 1
    if t-t0 > 5.0:
        print 'min-max of densities: ',  dens.min(),  dens.max(), inh.min(),  inh.max()
        fps = float(frames)/(t-t0)
        print 'FPS: %.2f (%d frames in %.2f seconds)' % (fps, frames, t-t0)
        frames,t0 = 0, t

window.mainloop()
