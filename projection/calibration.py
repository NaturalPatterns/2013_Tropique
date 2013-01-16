#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Particle-like simulations using pyglet.app

Calibration mode.

"""


DEBUG = False
#DEBUG = True

# ---------
# Scenarios
# ---------
scenario = 'croix'
#
#import socket
#
#UDP_IP=""
#UDP_PORT=7003
#
#sock = socket.socket( socket.AF_INET,socket.SOCK_DGRAM ) # UDP
#sock.bind( (UDP_IP,UDP_PORT) )
#sock.setblocking(0)
# 
#
#
#send_UDP_IP="10.42.43.1"
#send_UDP_PORT=7005
#send_sock = socket.socket( socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM ) # UDP
#                      
#                      
#                      
#UDP_IP = ""
#UDP_PORT = 7007
#print "UDP my port:", UDP_PORT
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM ) # UDP
#sock.bind((UDP_IP, UDP_PORT) )
##sock.settimeout(0)
#sock.setblocking(0)


from parametres import VPs, volume, p, kinects_network_config
import sys
sys.path.append('network/')

from network import Kinects
do_sock=True
if do_sock:
    k = Kinects(kinects_network_config)
else:
    positions = None


from scenarios import Scenario
s = Scenario(p['N'], scenario, volume, VPs, p)

from numpy import cos, pi

positions = []
T = 20. # periode en secondes
phi = 10/9. #.5*( 1 + sqrt(5) )
positions.append([s.center[0], s.center[1] , s.center[2]])

while True:
    if do_sock:
        position = k.read_sock() # TODO: c'est bien une liste de coordonnées [x, y, z] ?
        # TODO: put in network
        if (position!=None) : 
            print "the pos are ", position
#            for changing in position:
#                print 'pos de 0' , changing[0]
#                changing[0] /= 100
#                changing[1] /= 100
#                changing[2] /= 100
#            #positions.append(positions)
#            print"the good are ",   positions
    else:
        # HACK pour simuler ROGER:
        positions = []
#        positions = [[s.center[0], s.center[1], s.center[2]]] # une personne fixe
        T = 20. # periode en secondes
        phi = 10/9. #.5*( 1 + sqrt(5) )
        positions.append([s.center[0], s.center[1] * (1 - .75*cos(2*pi*s.t/T)), 1.2*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
        positions.append([s.center[0], s.center[1] * (1 - .75*cos(2*pi*s.t/T/phi)),0.9*s.center[2]]) # une autre personne dans un mouvement en phase
#    print positions


    s.do_scenario(positions=positions)
    
    if do_sock: k.trigger()
        
#    str_send = s.particles[0:6, :].tostring()
#    #print str_send
#    try :
#        Donnee, Client = sock.recvfrom (4096)
#    except (KeyboardInterrupt):
#        raise
#    except:
#        pass # detect = 0
#    else :
#        #print "ok", Client [0]
#        send_sock.sendto(str_send, (Client [0], send_UDP_PORT) )
