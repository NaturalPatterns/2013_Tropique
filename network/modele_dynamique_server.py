#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Particle-like simulation. Just the simulation.
Functional modes
@author: BIOGENE&lolo

"""
DEBUG = False
from time import gmtime, strftime

import sys
sys.path.append('..')

import time
import OSC
import socket
from parametres import VPs, volume, p, kinects_network_config, run_thread_network_config, scenario, calibration

send_sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP
client = OSC.OSCClient()
client.connect( ('10.42.0.70', 9001) ) # note that the argument is a tupple and not two arguments

from_IP=run_thread_network_config['ip_to_line_res']#
from_PORT=run_thread_network_config['port_to_line_res']
from_send = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP


do_sock=True
if do_sock:
    from network import Kinects
    k = Kinects(kinects_network_config)
else:
    positions = None

sys.path.append('..')
from modele_dynamique import Scenario
s = Scenario(p['N'], scenario, volume, VPs, p, calibration)

positions = []

positions.append([s.center[0], s.center[1] , s.center[2]]) # une personne dans un mouvement circulaire (elipse)
test_positions = ([s.center[0], s.center[1] , s.center[2]]) # une personne dans un mouvement circulaire (elipse)

#global events
events = [1, 1, 0, 0, 0, 0, 0, 0] # 8 types d'événéments

#if play == "croix":
#    positions.append([0, s.center[1] , 1.36 ])# une personne
#    do_sock=False
#--------------------------OSC SERVER
import OSC
import threading
# tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
receive_address = ('10.42.0.70', 6666)

# OSC Server. there are three different types of server.
sok = OSC.OSCServer(receive_address) # basic
##s = OSC.ThreadingOSCServer(receive_address) # threading
##s = OSC.ForkingOSCServer(receive_address) # forking

# this registers a 'default' handler (for unmatched messages),
# an /'error' handler, an '/info' handler.
# And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
#sok.addDefaultHandlers()
# define a message-handler function for the server to call.

def printing_handler(addr, tags, stuff, source):
    global events
#    print "---"
#    print "received new osc msg from %s" % OSC.getUrlStr(source)
#    print "with addr : %s" % addr
#    print "typetags %s" % tags

#    print "data %s" % stuff,strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
    events = (stuff)

sok.addMsgHandler("/seq", printing_handler) # adding our function


# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in sok.getOSCAddressSpace():
    print addr

# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = sok.serve_forever )
st.daemon=True

st.start()
do_slider = True
#----------------------
try:
    def sliders(p):
        import matplotlib as mpl
        mpl.rcParams['interactive'] = True
        mpl.rcParams['backend'] = 'macosx'
        #mpl.rcParams['backend_fallback'] = True
        mpl.rcParams['toolbar'] = 'None'
        import pylab as plt
        fig = plt.figure(1)
    #    AX = fig.add_subplot(111)
        plt.ion()
        # turn interactive mode on for dynamic updates.  If you aren't in interactive mode, you'll need to use a GUI event handler/timer.
        from matplotlib.widgets import Slider as slider_pylab
        ax, value = [], []
        n_key = len(p.keys())*1.
    #    print s.p.keys()
        for i_key, key in enumerate(p.keys()):
    #        print [0.1, 0.05+i_key/(n_key+1)*.9, 0.9, 0.05]
            ax.append(fig.add_axes([0.15, 0.05+i_key/(n_key-1)*.9, 0.6, 0.05], axisbg='lightgoldenrodyellow'))
            if p[key] > 0:
                value.append(slider_pylab(ax[i_key], key, 0., (p[key] + (p[key]==0)*1.)*10, valinit=p[key]))
            else:
                value.append(slider_pylab(ax[i_key], key,  (p[key] + (p[key]==0)*1.)*10,  -(p[key] + (p[key]==0)*1.)*10, valinit=p[key]))

        def update(val):
            for i_key, key in enumerate(p.keys()):
                p[key]= value[i_key].val
                print key, p[key]#, value[i_key].val
            plt.draw()

        for i_key, key in enumerate(p.keys()): value[i_key].on_changed(update)

        plt.show(block=False) # il faut plt.ion() pour pas avoir de blocage

        return fig

    if s.scenario=='leapfrog' and do_slider:
        fig = sliders(s.p)
except Exception, e:
    print('problem while importing sliders ! Error = ', e)

start_time = time.time()
#print events
while True:
    #global events
    if DEBUG:
        elapsed_time = time.time() - start_time
        start_time = time.time()
        print "FPS =" , int (1/elapsed_time)

    if do_sock:
        k.trigger()
        test_positions = k.read_sock() # TODO: c'est bien une liste de coordonnées [x, y, z] ?
        if (test_positions!=None):
            positions = []
#            print test_positions
            for position in test_positions:
                positions.append([position[0], position[1],position[2] ])
#            print positions[0][1]
#    else:
#        if play == "croix":
#                positions.append([0, s.center[1] , 1.36 ])# une personne
#        # HACK pour simuler ROGER:
#
#        from numpy import cos, pi
#        positions = []
#        T = 20. # periode en secondes
#        phi = 10/9. #.5*( 1 + sqrt(5) )
#        positions.append([s.center[0], s.center[1] * (1. + 1.2*cos(2*pi*s.t/T)), 1.1*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
#        positions.append([s.center[0], s.center[1] * (1. + .0*cos(2*pi*s.t/T/phi)), 1.*s.center[2]]) # une autre personne dans un mouvement en phase
##        positions.append([s.center[0], s.center[1] * (1. + .75*cos(2*pi*s.t/T)), 1.2*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
##        positions.append([s.center[0], s.center[1] * (1. + .75*cos(2*pi*s.t/T)), 1.2*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
##        positions.append([s.center[0], s.center[1] * (1. + .75*cos(2*pi*s.t/T)), 1.2*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
##        positions.append([s.center[0], s.center[1] * (1. + .75*cos(2*pi*s.t/T)), 1.2*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
##        positions.append([s.center[0], s.center[1] * (1. + .75*cos(2*pi*s.t/T)), 1.2*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
##        positions.append([s.center[0], s.center[1] * (1. + .0*cos(2*pi*s.t/T/phi)),0.9*s.center[2]]) # une autre personne dans un mouvement en phase
##        positions.append([s.center[0], s.volume[1]*.75, s.volume[2]*.75]) # une personne dans un mouvement circulaire (elipse)

    s.do_scenario(positions=positions, events=events)

    # envoi aux VPs
    str_send = s.particles[0:6, :].tostring('F')
    from_send.sendto(str_send, (from_IP, from_PORT) )

    # envoi à OSC
    msg = OSC.OSCMessage()
    msg.setAddress("/segment")
    msg.append((s.particles[0:6, -2:].T))

    try :
        client.send(msg)
    except KeyboardInterrupt :
        print "\nClosing OSCServer."
        s.close()
        print "Waiting for Server-thread to finish"
        st.join() ##!!!
        print "Done"
        raise
    except:
        pass
#        print "no client OSC"

    #vps.server(s.particles)
