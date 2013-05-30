#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 14:41:46 2012

@author: tropic
"""
import sys
sys.path.append('..')
from parametres import VPs, volume, p, run_thread_network_config

import socket
from network import VP
import numpy as np

vps= VP(run_thread_network_config['ip_to_line_res'] , 7005 , 7006)

#from_IP="10.42.0.101"
listen_run_thread_PORT=run_thread_network_config['port_to_line_res']
listen_run_thread = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP
listen_run_thread.bind(("", listen_run_thread_PORT))
listen_run_thread.setblocking(0)

from modele_dynamique import Scenario
s = Scenario(p['N'], 'croix', volume, VPs, p)
test_positions = ([s.center[0], s.center[1] , s.center[2]]) # une personne dans un mouvement circulaire (elipse)
positions = []
positions.append([s.center[0], s.center[1] , s.center[2]])
s.do_scenario(positions=positions)
Donnee=s.particles[0:6, :].tostring('F')

while True:
    try :
        Donnee, Client = listen_run_thread.recvfrom (8192)
    except (KeyboardInterrupt):
        raise
    except:
        pass # detect = 0
    else :
        rien = 0

    vps.server(Donnee)
