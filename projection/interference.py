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
downscale = 10
N_X, N_Y = 1200/downscale, 1920/downscale # size of the simulation grid
width = .01
#R_min = 1.

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
X, Y = numpy.mgrid[0:N_X, 0:N_Y]
y = N_Y/2
fig = glumpy.figure((N_Y*downscale, N_X*downscale)) # , fullscreen = fullscreen
im_buffer = glumpy.Image(dens, interpolation='bicubic', colormap=cmap)
############################################################################
def rayon(x, y, x_0, y_0):
    R = numpy.sqrt( (X-x_0)**2 + (Y-y_0)**2)
    r = numpy.sqrt( (x-x_0)**2 + (y-y_0)**2)
    d = numpy.abs((x-x_0)*(y-y_0) - (x_0-X)*(y_0-Y)) / r
    R1 = numpy.sqrt( R**2 - d**2 )
    return numpy.exp(- ( d )**2 / 2 / R1**2 / width**2 ) / R #numpy.sqrt( R**2 + 12 )
#    return R1
############################################################################

# main loop
@fig.event
def on_draw():
    fig.clear()
    im_buffer.draw( x=0, y=0, z=0, width=fig.width, height=fig.height )

@fig.event
def on_idle(elasped):
    global dens, y
    x_0, y_0 = -10, N_Y/2
#    y += numpy.random.randn()*N_Y/100
#    y = numpy.mod(y, N_Y)
#    print y
    dens *= 0.
    dens  += rayon(N_X, y, x_0, y_0)

#    print dens.max(), dens.min()
#    dens  = numpy.ones((N_X, N_Y), dtype=numpy.float32) # density
#    dens[numpy.random.randint(N_X),numpy.random.randint(N_Y)] = -50
#    dens = dens.astype(numpy.float32)
    im_buffer.update()
    fig.draw()

glumpy.show()
