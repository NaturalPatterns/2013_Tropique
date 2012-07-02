#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Particle-like simulation. Just the simulation.

Functional mode
@author: BIOGENE&lolo

"""
DEBUG = False
#DEBUG = True

import sys
sys.path.append('..')

import time
#from network import VP
#vps= VP(None)

import socket
from_IP="10.42.0.102"
from_PORT=8005
from_send = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP

from parametres import VPs, volume, p, kinects

do_sock=True
#do_sock=False 
if do_sock:
    from network import Kinects
    k = Kinects(kinects)
else:
    positions = None


from scenarios import Scenario

s = Scenario(p['N'], 'leapfrog', volume, VPs, p)
from numpy import cos, pi
positions = []

positions.append([s.center[0], s.center[1] , s.center[2]]) # une personne dans un mouvement circulaire (elipse)
test_positions = ([s.center[0], s.center[1] , s.center[2]]) # une personne dans un mouvement circulaire (elipse)

start_time = time.time()

while True:
    
    if DEBUG: 
        elapsed_time = time.time() - start_time
        start_time = time.time()
        
        print "FPS =" , int (1/elapsed_time)
    if do_sock:
        k.trigger()
        test_positions = k.read_sock() # TODO: c'est bien une liste de coordonnées [x, y, z] ?
        if (test_positions!=None):
            positions = []
#            print "the test_pos", test_positions
            #positions = [2.0 , 2.0 , 0.0]
            for position in test_positions:
                positions.append([position[0], position[1],position[2] ])
#        print "the new pos are ", positions
    else:
        # HACK pour simuler ROGER:
        positions = []
#        positions = [[s.center[0], s.center[1], s.center[2]]] # une personne fixe
        T = 20. # periode en secondes
        phi = 10/9. #.5*( 1 + sqrt(5) )
        positions.append([s.center[0], s.center[1] * (1. + 1.2*cos(2*pi*s.t/T)), 1.1*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
        positions.append([s.center[0], s.center[1] * (2.2 + 1.0*cos(2*pi*s.t/T/phi)), 1.2*s.center[2]]) # une autre personne dans un mouvement en phase
        positions.append([s.center[0], s.center[1] * (1. + .0*cos(2*pi*s.t/T/phi)), 1.*s.center[2]]) # une autre personne dans un mouvement en phase
#        positions.append([s.center[0], s.volume[1]*.75, s.volume[2]*.75]) # une personne dans un mouvement circulaire (elipse)
#        positions.append([s.center[0], s.volume[1]*.25, s.volume[2]*.25]) # une autre personne dans un mouvement en phase
#        positions.append([s.center[0], s.center[1] * (1. + .75*cos(2*pi*s.t/T)), 1.2*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
#        positions.append([s.center[0], s.center[1] * (1. + .75*cos(2*pi*s.t/T)), 1.2*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
#        positions.append([s.center[0], s.center[1] * (1. + .75*cos(2*pi*s.t/T)), 1.2*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
#        positions.append([s.center[0], s.center[1] * (1. + .75*cos(2*pi*s.t/T)), 1.2*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
#        positions.append([s.center[0], s.center[1] * (1. + .75*cos(2*pi*s.t/T)), 1.2*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
#        positions.append([s.center[0], s.center[1] * (1. + .75*cos(2*pi*s.t/T)), 1.2*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
#        positions.append([s.center[0], s.center[1] * (1. + .75*cos(2*pi*s.t/T)), 1.2*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
#        positions.append([s.center[0], s.center[1] * (1. + .0*cos(2*pi*s.t/T/phi)),0.9*s.center[2]]) # une autre personne dans un mouvement en phase
#        positions.append([s.center[0], s.volume[1]*.75, s.volume[2]*.75]) # une personne dans un mouvement circulaire (elipse)

    s.do_scenario(positions=positions)
        
    str_send = s.particles[0:6, :].tostring('F')
    from_send.sendto(str_send, (from_IP, from_PORT) ) 

#    if DEBUG: print "the new pos are ", positions

    #vps.server(s.particles)
