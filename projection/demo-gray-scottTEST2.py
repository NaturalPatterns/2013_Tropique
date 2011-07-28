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
from dana import *
import glumpy
import sys

n  = 128
dt = 1#*second
t  = 50000#*second

width = n*16/9#4/3
fullscreen = True
#fullscreen = False
interpolation='bicubic'
interpolation='nearest'

# Parameters from http://www.aliensaint.com/uo/java/rd/
# -----------------------------------------------------
# Du, Dv, F, k = # 
zoo = {'Pulses': [0.16, 0.08, 0.02, 0.055],
       'Worms 1': [0.16, 0.08, 0.052, 0.065], 
       'Worms 2':[0.16, 0.08, 0.054, 0.063],
       'Zebrafish':[0.16, 0.08, 0.035, 0.060],
       'Bacteria 2': [0.14, 0.06, 0.035, 0.065 ],
       'Coral': [0.16, 0.08, 0.060, 0.062],
       'Fingerprint': [0.19, 0.05, 0.060, 0.062],
       'Spirals': [0.10, 0.10, 0.018, 0.050],
       'Spirals Dense': [0.12, 0.08, 0.020, 0.050],
       'Spirals Fast': [0.10, 0.16, 0.020, 0.050],
       'Unstable': [0.16, 0.08, 0.020, 0.055],
       'Bacteria 1': [0.16, 0.08, 0.035, 0.065],
}


def init(Du, Dv, F, k):
    Z = Group((width,n), '''du/dt = Du*Lu - Z + F*(1-U) : float32
                        dv/dt = Dv*Lv + Z - (F+k)*V : float32
                        U = maximum(u,0) : float32
                        V = maximum(v,0) : float32
                        Z = U*V*V : float32
                        Lu; Lv; ''')
    K = np.array([[np.NaN,  1., np.NaN], 
                  [  1.,   -4.,   1.  ],
                  [np.NaN,  1., np.NaN]])
    SparseConnection(Z('U'),Z('Lu'), K, toric=True)
    SparseConnection(Z('V'),Z('Lv'), K, toric=True)
    Z['u'] = 1.0
    Z['v'] = 0.0
    Z['u'][width/4:3*width/4,n/4:3*n/4] = 0.50
    Z['v'][width/4:3*width/4,n/4:3*n/4] = 0.25    
    Z['u'] += 0.01*np.random.random((width,n))
    Z['v'] += 0.01*np.random.random((width,n))
    Z['U'] = Z['u']
    Z['V'] = Z['v']
    return Z, n 

Du, Dv, F, k = zoo['Fingerprint']
Z, n = init(Du, Dv, F, k)
Zu = glumpy.Image(Z['u'], interpolation=interpolation,
                  cmap=glumpy.colormap.Grey_r, vmin=0.0 , vmax=1.0)
window = glumpy.Window(width,n, fullscreen = fullscreen)

@window.event
def on_mouse_drag(x, y, dx, dy, button):
    global Z, n, width
    center =( int((1-y/float(window.width)) * (width-1)),
              int(x/float(window.height) * (n-1)) )
    radius = 8
    def distance(x,y):
        return np.sqrt((x-center[0])**2+(y-center[1])**2)
    D = np.fromfunction(distance,(width,n))
    M = np.where(D<=radius,True,False).astype(np.float32)
    Z['U'] = Z['u'] = (1-M)*Z['u'] + M*0.50
    Z['V'] = Z['v'] = (1-M)*Z['v'] + M*0.25
    Zu.update()

@window.event
def on_key_drag(key, modifiers):
    global zoo, Z, n, width
    if key == glumpy.key.ESCAPE:
        sys.exit()
    elif key == glumpy.key.N:
        i = np.random.randint(0, len(zoo.keys()))
        Du, Dv, F, k = zoo.values()[i]
        print zoo.keys()[i]
        #Z, n = init(Du, Dv, F, k)
        Z._namespace['Du'] = Du
        Z._namespace['Dv'] = Dv
        Z._namespace['F'] = F
        Z._namespace['k'] = k
        
@window.event
def on_draw():
    window.clear()
    Zu.blit(0,0,window.width,window.height)

@window.event
def on_idle(*args):
    for i in range(10):
        Z.evaluate(dt=dt)
    Zu.update()
    window.draw()
window.mainloop()
#
#plt.ion()
#fig = plt.figure(figsize=(8,8))
#im = plt.imshow(Z['U'], interpolation='bicubic', cmap=plt.cm.gray)
#@clock.every(10*second)
#def frame(t):
#    im.set_data(Z['U'])
#    im.changed()
#    plt.draw()
#
#run(time=t, dt=dt)
#plt.ioff()
#plt.show()
