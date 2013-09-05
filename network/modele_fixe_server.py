#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script renvoyant des données de calibration au réseau des VPs.

@author: BIOGENE&lolo

"""

import sys
sys.path.append('..')
from parametres import VPs, volume, p , run_thread_network_config, DEBUG, calibration, scenario

import socket
from_IP=run_thread_network_config['ip_to_line_res']
from_PORT=run_thread_network_config['port_to_line_res']
from_send = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP

from modele_dynamique import Scenario
s = Scenario(p['N'], scenario, volume, VPs, p, calibration)
while True:
    s.do_scenario()#positions=[], events=events)
    # print s.particles[0:6, 0], s.particles[0:6, -1]
    # envoi aux VPs
    str_send = s.particles[0:6, :].tostring('F')
    from_send.sendto(str_send, (from_IP, from_PORT) )
