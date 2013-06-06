#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import time
start_time = time.time()
from time import gmtime, strftime
import OSC
import socket
from parametres import VPs, volume, p, kinects_network_config, run_thread_network_config, scenario, calibration, DEBUG
#----------------------
send_sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP
client = OSC.OSCClient()
client.connect( ('10.42.0.70', 9001) ) # note that the argument is a tupple and not two arguments
from_IP=run_thread_network_config['ip_to_line_res']#
from_PORT=run_thread_network_config['port_to_line_res']
from_send = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP
#----------------------
from network import Kinects
k = Kinects(kinects_network_config)
#----------------------
from modele_dynamique import Scenario
s = Scenario(p['N'], scenario, volume, VPs, p, calibration)
#--------------------------OSC SERVER
import threading
# tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
receive_address = ('10.42.0.70', 6666)
# OSC Server. there are three different types of server.
sok = OSC.OSCServer(receive_address) # basic
events = [0, 0, 0, 0, 0, 0, 0, 0] # 8 types d'événéments
def printing_handler(addr, tags, stuff, source):
    global events
    events = (stuff)
sok.addMsgHandler("/seq", printing_handler) # adding our function
#----------------------
# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in sok.getOSCAddressSpace():
    print addr
#----------------------
# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = sok.serve_forever )
st.daemon=True
st.start()
#----------------------
do_slider = True
do_slider = False
try:
    from parametres import sliders
    if s.scenario=='leapfrog' and do_slider:
        fig = sliders(s.p)
except Exception, e:
    print('problem while importing sliders ! Error = ', e)
#----------------------
positions_old = []
while True:
    #if DEBUG:
        #elapsed_time = time.time() - start_time
        #start_time = time.time()
        #if elapsed_time>0: print "FPS =" , int (1/elapsed_time)
    k.trigger()
    positions = []
    test_positions = k.read_sock()
    if (test_positions!=None):
        for position in test_positions:
            positions.append([position[0], position[1],position[2] ])
    #if DEBUG: print positions, events
    # HACK pour pas perdre de trames de detection
    if positions == []: positions = positions_old
    else: positions_old = positions
    if DEBUG: print events
    s.do_scenario(positions=positions, events=events)
    #if DEBUG: print  s.particles[0:3, :].mean(axis=1), s.particles[3:6, :].mean(axis=1), s.particles[0:3, :].std(axis=1), s.particles[3:6, :].std(axis=1)
    # envoi aux VPs
    str_send = s.particles[0:6, :].tostring('F')
    from_send.sendto(str_send, (from_IP, from_PORT) )
    # envoi à OSC
    msg = OSC.OSCMessage()
    msg.setAddress("/segment")
    msg.append((s.particles[0:6, -2:].T))
    try:
        client.send(msg)
    except KeyboardInterrupt:
        print "\nClosing OSCServer."
        s.close()
        print "Waiting for Server-thread to finish"
        st.join() ##!!!
        print "Done"
        raise
    except:
        pass

