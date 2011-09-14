#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (C) 2011 _ Laurent Perrinet
"""

Interferences

Du coup, j'ai pense a un truc, c'est d'utiliser au contraire la
cohérence de faisceaux de lignes : une expeirence a faire et de mettre
deux vps en face l'un de lautre qui montrent un genre de code barre
assez fin. Les faisceaux divergent, le seul endroit cohérent quand ils
interfèrent et le milieu (la bissectrice entre les 2 VPs)  le reste
doit être gris.


"""
import numpy, glumpy

############################################################################
N_X, N_Y = 400, 600 # size of the simulation grid

# visualization parameters
downscale = 2
fullscreen = False # True #
interpolation= 'bicubic' # 'nearest' #
cmap = glumpy.colormap.Colormap("BlueGrey",
                                (0., (0.,0.,0.)), (1., (0.75,0.75,1.00)))
############################################################################

############################################################################
# initialization
dens  = numpy.zeros((N_X, N_Y), dtype=numpy.float32) # density

Z = numpy.zeros((N_X, N_Y), dtype=numpy.float32)
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


# main loop
@window.event
def on_idle(*args):
    global dens, inh, dens_noise, inh_noise, dt, diff, diff_inh, rho_a, mu_a, rho_h, mu_h
    window.clear()
    if window.last_drag:
        x,y,dx,dy,button = window.last_drag
        j = min(max(int(N_Y*x/float(window.width)),0),N-1)
        i = min(max(int(N_X*(window.height-y)/float(window.height)),0),N-1)
        if  button:#False:#not button:
            dens[i,j] = inh[i,j] = source
#            dens_[:,j] = source # creating a vertical line
    
    window.last_drag = None
    
    # Heat equation
#    dens +=  diff * laplace(dens, mode='wrap')
    dens  = numpy.zeros((N_X, N_Y), dtype=numpy.float32) # density
    x_0, y_0 = 0, 0
    for x, y in zip([0.5, 0.5]):
        dens += rayon(x_0, y_0, x, y)

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
