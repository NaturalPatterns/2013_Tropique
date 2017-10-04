#!/usr/bin/env python
# -*- coding: utf8 -*-
""" le client centralise  l'ensemble des commandes a envoyé au différents serveur kinect difini dans myarc
"""
import sys
sys.path.append('..')
from parametres_vasarely import info_kinects , DEBUG
import socket
import os

nbr_kinect = 0
import time as time

from threading import Thread

global DEBUG
global f
f = open('record_her', 'w')
class testkin(Thread):
    def __init__ (self,ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.status = -1
        self.HOST = '10.42.0.20'
        self.port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto ('data' , (self.ip, self.port ) )
        sock.settimeout(0.5)
        try :
            received = sock.recv(1024)
        except KeyboardInterrupt:
            print "stop acquisition kinect"
        except :
            print "PROBLEME no data in ", self.ip
            self.status = 0
        else :
            if (DEBUG and received !="" ) : print "received = ", received," from ", self.port
            if (DEBUG and received =="" ) : print "received 0", " from ",self.port
            self.status = received

def list_kinect():
    os.system('clear')
    print "\n \t liste des kinects dans architecture \n"
    print "il y a ", (len (info_kinects)) , " kinects configuré \n",
    for ligne in range (len (info_kinects)):
        print ligne, info_kinects[ligne]

def stream_acqui():
#    os.system('clear')
    print "listen to kinects server "
    teston =0
    last_time = 0
    while (teston < 1) :
        a = time.time()
        b = a - last_time
#        print "the time lapsed = ",b , 1/float(b)
        last_time = a
        serverkinects = []
        for kin in info_kinects :
            ip = kin['address']
            port = kin['port']
            current = testkin(ip,9998+port)
            serverkinects.append(current)
            current.start()
        all_pos=""
        for server in serverkinects:
            server.join()
            try: var = int(server.status)
            except:all_pos +=server.status
            else: pass
        all_pos = all_pos[0:(len(all_pos) -1)]
        if all_pos !="":
#            print "send  =", all_pos
            sock_to_affi.sendto((all_pos ), (affi_host, affi_port))
            f.write(str(b)+"   " + all_pos + " \n " )


def segment():
    os.system('clear')
    print "listen to kinects server "
    for kin in info_kinects :
        print kin['address'], kin['port']
        HOST = kin['address']
        PORT = kin['port']
        sock.sendto("segm" , (HOST, PORT))
        sock.settimeout(20)
        try :
            received = sock.recv(1024)
        except :
            print "PROBLEME no data in ", HOST, PORT
        else :
            print "Received: %s" % received

def send_kinect(com):
    last_kinect=""
    for kin in info_kinects:
        if kin['address'] != last_kinect :
            print "send to", kin['address'] ," comm ", com
            sock.sendto(str(com) , (kin['address'], 3002))
            last_kinect = kin['address']
def display():
    os.system('clear')
    print "display server "
    send_kinect(2)
def start_kinect():
    os.system('clear')
    print "try to start kinects server "
    send_kinect(1)
def kill_kinect():
    os.system('clear')
    print "try to kill kinects server "
    send_kinect(0)



if __name__ == "__main__":
    os.system('clear')
    # SOCK_DGRAM is the socket type to use for UDP sockets
    sock_to_affi = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    sock_pd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    affi_host = 'localhost'
    affi_port = 3004
    list_kinect()
    if DEBUG: print "send to ",affi_host, affi_port
    stream_acqui()
    print "send to ",my_host, my_port
    stream_acqui()

    while 1 :
        print "\n \t \t client.py = CLIENT KINECTS  in TROPIC \n"
        print "0 - stop prog"
        print "1 - liste des kinects"
        print "..."
        print "5 - start kinect DISPLAY = 1"
        print "6 - start kinect"
        print "7 - kill kinect"
        print "8 - segmentation/calib"
        print "9 - stream aquisition (ctrl-c to quit)"

        try:
            choice = input ( "que faire ??")
        except:
            os.system('clear')
            print "mauvais choix"
        else:
            if choice == 0 :
                os.system('clear')
                break
            if choice == 1 :
                list_kinect()
            if choice == 5 :
                display()
            if choice == 6 :
                start_kinect()
            if choice == 7 :
                kill_kinect()
            if choice ==8 :
                segment()
            if choice ==9 :
                stream_acqui()





