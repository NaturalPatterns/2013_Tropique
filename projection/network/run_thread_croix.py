#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Particle-like simulation. Just the simulation.
Functional mode
@author: BIOGENE&lolo

"""
DEBUG = False

import sys
sys.path.append('..')

import time
import OSC
import socket
from parametres import VPs, volume, p, kinects_network_config , run_thread_network_config

#
#send_sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP
#client = OSC.OSCClient()
#client.connect( ('10.42.0.70', 9001) ) # note that the argument is a tupple and not two arguments

from_IP=run_thread_network_config['ip_to_line_res']
from_PORT=run_thread_network_config['port_to_line_res']
from_send = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP



from scenarios import Scenario
s = Scenario(p['N'], 'croix', volume, VPs, p)
from numpy import cos, pi
positions = []

positions.append([s.center[0], s.center[1] , s.center[2]]) # une personne dans un mouvement circulaire (elipse)
test_positions = ([s.center[0], s.center[1] , s.center[2]]) # une personne dans un mouvement circulaire (elipse)



do_sock=False
if do_sock:
    from network import Kinects
    k = Kinects(kinects_network_config)
else:
    positions = None
    
global events
events = [0, 0, 0, 0, 0, 0, 0, 0] # 8 types d'événéments

##--------------------------OSC SERVER
#import OSC
#import threading
## tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
#receive_address = ('127.0.0.1', 6666)
# 
## OSC Server. there are three different types of server.
#sok = OSC.OSCServer(receive_address) # basic
###s = OSC.ThreadingOSCServer(receive_address) # threading
###s = OSC.ForkingOSCServer(receive_address) # forking
# 
## this registers a 'default' handler (for unmatched messages),
## an /'error' handler, an '/info' handler.
## And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
##sok.addDefaultHandlers()
## define a message-handler function for the server to call.
#def printing_handler(addr, tags, stuff, source):
#    global events
##    print "---"
##    print "received new osc msg from %s" % OSC.getUrlStr(source)
##    print "with addr : %s" % addr
##    print "typetags %s" % tags
#    print "data %s" % stuff
#    events = (stuff)
#    
#sok.addMsgHandler("/seq", printing_handler) # adding our function
## just checking which handlers we have added
#print "Registered Callback-functions are :"
#for addr in sok.getOSCAddressSpace():
#    print addr
# 
## Start OSCServer
#print "\nStarting OSCServer. Use ctrl-C to quit."
#st = threading.Thread( target = sok.serve_forever )
#st.daemon=True
#
#st.start()
##----------------------

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
            for position in test_positions:
                positions.append([position[0], position[1],position[2] ])
    else:
        # HACK pour simuler ROGER:
        positions = []
#        positions = [[s.center[0], s.center[1], s.center[2]]] # une personne fixe
        positions.append([0, s.center[1] , 1.36 ])# une personne fixe
#        positions.append([s.center[0], s.volume[1]*.25, s.volume[2]*.25]) # une autre personne dans un mouvement en phase


    s.do_scenario(positions=positions , events=events)
    
    # envoi aux VPs
    str_send = s.particles[0:6, :].tostring('F')
    from_send.sendto(str_send, (from_IP, from_PORT) )
    
#    # envoi à OSC
#    msg = OSC.OSCMessage()
#    msg.setAddress("/segment")
#    msg.append((s.particles[0:6, -2:].T))
#    
#    try :
#        client.send(msg) 
#    except KeyboardInterrupt :
#        print "\nClosing OSCServer."
#        s.close()
#        print "Waiting for Server-thread to finish"
#        st.join() ##!!!
#        print "Done"
#        raise
#    except:
#        pass
#        print "no client OSC"

    #vps.server(s.particles)
