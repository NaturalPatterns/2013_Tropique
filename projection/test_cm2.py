#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (C) 2011 _ Laurent Perrinet
"""

CM2 - base sur Interferences

des tests faits en decembre, ca me rapelle des "experiences" de dessin geometrique de la periode CM2...

recette:
--------
* sur une feuille quadrillee, faire 2 points,
* mettre des reperes sur les bords de la feuille tous les centimetres,
* tracer les segments de chaque point a chaque repere 

(marche avec N points)

"""
import numpy, glumpy

############################################################################
downscale = 4
N_X, N_Y = 1200/downscale, 1920/downscale # size of the simulation grid
x_VPs = [ N_X/2, N_X/2, N_X/2 ]
y_VPs = [ N_Y/3, N_Y/2, 2*N_Y/3 ]
width = 4.
N_sources = 16
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

coord = numpy.linspace(0, 2*(N_X+N_Y), N_sources)
#x = numpy.random.rand(N_sources)*N_X
t, t0, frames, elapsed = 0,0,0, 0
N_VPs = len(x_VPs)
fig = glumpy.figure((N_Y*downscale, N_X*downscale)) # , fullscreen = fullscreen
im_buffer = glumpy.Image(dens, interpolation='bicubic', colormap=glumpy.colormap.Grey)#cmap)
############################################################################
def rayon(x, y, x_0, y_0, r_min = 30):
    R = numpy.sqrt( (X-x_0)**2 + (Y-y_0)**2 + r_min**2)
    r = numpy.sqrt( (x-x_0)**2 + (y-y_0)**2 + r_min**2)
    D = numpy.abs((x-x_0)*(y_0-Y) - (x_0-X)*(y-y_0)) / r
    R1 = numpy.sqrt( R**2 - D**2 )
    return numpy.exp(- D**2 * r**2 / 2 / R1**2 / width**2 ) / R 
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
    global dens, lum, coord
    coord += numpy.random.randn(N_sources)*2*(N_X+N_Y)*speed
    coord = numpy.mod(coord, 2*(N_X+N_Y))
    x_, y_ = numpy.zeros(N_sources), numpy.zeros(N_sources)
    for i_coord, coord_ in enumerate(coord):
        if coord_ < N_X:
            x_[i_coord], y_[i_coord] = coord_, 0
        elif N_X <= coord_ < N_X+N_Y:
            x_[i_coord], y_[i_coord] = 0, coord_-N_Y
        elif N_X+N_Y <= coord_ < 2*N_X+N_Y:
            x_[i_coord], y_[i_coord] = N_X - (coord_-N_Y-N_X), N_Y
        else:
            x_[i_coord], y_[i_coord] = N_X, N_Y - (coord_- 2*N_X-N_Y)
            
    dens *= 0.
    for x__, y__ in zip(x_, y_):
        for x_0, y_0 in zip(x_VPs, y_VPs):
            dens  += rayon(x__, y__, x_0, y_0) / N_sources / N_VPs
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
