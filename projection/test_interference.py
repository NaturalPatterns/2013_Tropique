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
downscale = 4
N_X, N_Y = 1200/downscale, 1920/downscale # size of the simulation grid
recul = 20
x_VPs = [ 0 , N_X/4, N_X/2, 3*N_X/4, N_X,  0 , N_X/4, N_X/2, 3*N_X/4, N_X ]
y_VPs = [ -recul , -recul, -recul, -recul, -recul, N_Y+recul, N_Y+recul, N_Y+recul, N_Y+recul, N_Y+recul ]
#x_VPs = [ 0 , N_X/2, N_X,  0 , N_X/2, N_X ]
#y_VPs = [ -recul , -recul, -recul, N_Y+recul, N_Y+recul, N_Y+recul ]
width = 4.
N_sources = 4
speed = 1e-2
noise=1e-0
# visualization parameters
fullscreen = False # True #
interpolation= 'bicubic' # 'nearest' #
#cmap = glumpy.colormap.Colormap("BlueGrey",
#                                (0., (0.,0.,0.)), (1., (0.75,0.75,1.00)))
cmap = glumpy.colormap.Colormap("blue",
                                (0.00, (0.2, 0.2, 1.0)),
                                (1.00, (1.0, 1.0, 1.0)))
############################################################################
# initialization
dens  = numpy.zeros((N_X, N_Y), dtype=numpy.float32) # density
lum  = numpy.zeros((N_X, N_Y), dtype=numpy.float32) # luminance
X, Y = numpy.mgrid[0:N_X, 0:N_Y]
#x = numpy.linspace(0, N_X, N_sources)
x = numpy.random.rand(N_sources)*N_X
t, t0, frames, elapsed = 0,0,0, 0
N_VPs = len(x_VPs)
fig = glumpy.figure((N_Y*downscale, N_X*downscale)) # , fullscreen = fullscreen
im_buffer = glumpy.Image(dens, interpolation='bicubic', colormap=glumpy.colormap.Grey)#cmap)
############################################################################
def rayon(x, y, x_0, y_0):
    R = numpy.sqrt( (X-x_0)**2 + (Y-y_0)**2)
    r = numpy.sqrt( (x-x_0)**2 + (y-y_0)**2)
    d = numpy.abs((x-x_0)*(y_0-Y) - (x_0-X)*(y-y_0)) / r
    R1 = numpy.sqrt( R**2 - d**2 )
    return numpy.exp(- ( d )**2 / 2 / R1**2 * r**2 / width**2 ) / R #numpy.sqrt( R**2 + 12 )
#    return R1
############################################################################

# main loop
@fig.event
def on_draw():
    fig.clear()
    im_buffer.draw( x=0, y=0, z=0, width=fig.width, height=fig.height )

@fig.event
def on_key_press(key, modifiers):
    if key == glumpy.window.key.TAB:
        if fig.window.get_fullscreen():
            fig.window.set_fullscreen(0)
        else:
            fig.window.set_fullscreen(1)

@fig.event
def on_idle(elapsed):
    global dens, lum, x
    x += numpy.random.randn(N_sources)*N_X*speed
    x = numpy.mod(x, N_Y)

    dens *= 0.
    for x_ in x:
        for x_0, y_0 in zip(x_VPs, y_VPs):
            dens  += rayon(x_, (x_-N_X/2)**2 / N_Y + N_Y/2, x_0, y_0) / N_sources / N_VPs
    dens = numpy.log(dens+noise)
    im_buffer.update()
    fig.redraw()
    
    global t, t0, frames
    t += elapsed
    frames = frames + 1
    if t-t0 > 5.0:
        fps = float(frames)/(t-t0)
        print 'FPS: %.2f (%d frames in %.2f seconds)' % (fps, frames, t-t0)
        frames,t0 = 0, t
glumpy.show()