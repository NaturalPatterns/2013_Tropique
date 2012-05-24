# -*- coding: utf-8 -*-
"""
Created on Fri May 18 14:41:46 2012

@author: tropic
"""
import sys
sys.path.append('..')

import socket
from network import VP
vps= VP(None)
import numpy as np

from_IP="10.42.0.101"
from_PORT=8005
from_send = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP
from_send.bind(("", from_PORT))
from_send.setblocking(0)

from parametres import VPs, volume, p
from scenarios import Scenario
s = Scenario(p['N'], 'leapfrog', volume, VPs, p)
test_positions = ([s.center[0], s.center[1] , s.center[2]]) # une personne dans un mouvement circulaire (elipse)
positions = []
positions.append([s.center[0], s.center[1] , s.center[2]])
s.do_scenario(positions=positions)
Donnee=s.particles[0:6, :].tostring('F')

while True:
    try :
        Donnee, Client = from_send.recvfrom (8192)
    except (KeyboardInterrupt):
        raise
    except:
        pass # detect = 0
    else :
        print "receive"
#    print "hehe"

#    print Donnee
#    s.do_scenario(positions=positions)
#    Donnee=s.particles[0:6, :].tostring('F')
    vps.server(Donnee)
