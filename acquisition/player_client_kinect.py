#!/usr/bin/env python
# -*- coding: utf8 -*-
""" le client centralise  l'ensemble des commandes a envoyé au différents serveur kinect difini dans myarc
"""
import sys
sys.path.append('..')
import socket
import os
from parametres_vasarely import info_kinects , DEBUG

nbr_kinect = 0
import time as time

from threading import Thread

global DEBUG
global f
f = open('record_her', 'r')

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
    global  f
    os.system('clear')
    print "listen to kinects server whou "
    # SOCK_DGRAM is the socket type to use for UDP sockets
#    testit.lifeline = re.compile(r"(\d) received")
    teston =0
    last_time = 0
    nbr_data = 0
    i = 0
    total = 0
    goodsend =0

    while (i==0) :
        a = time.time()
        serverkinects = []
        texttest = f.readline()
        all_pos  = texttest
        try : 
            the_pos =  float(all_pos.partition("   ")[0])
            nbr_data +=1
            if the_pos <= 1 :
                time.sleep(the_pos)
            try :
                sendor, Client = sock_confirm.recvfrom (1024)
            except (KeyboardInterrupt):
                raise
            except:
                pass
            else :
                goodsend = 1
            if goodsend == 1:
                sock_pd.sendto((all_pos.partition("   ")[2] ), (my_host, my_port))
                goodsend =0
            b = a - last_time 
            total +=b
#            print "the time lapsed = , for time ",b , the_pos, all_pos.partition("   ")[2]
            last_time = a
        except : 
            f.close()
            print("redemarre" , total)
            totam =0
            f = open('record_her', 'r')
            print "reommence" ,  teston, nbr_data
            teston +=1
            nbr_data =0
            
        all_pos = all_pos[0:(len(all_pos) -1)]
        
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
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_pd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_confirm = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_confirm.bind(("127.0.0.1", 5555))
    sock_confirm.setblocking(0)

    host_pd = '89.226.106.164'
    port_pd = 3002
    host_affi = '10.42.0.100'
    port_affi = 3003
    my_host = '127.0.0.1'
    my_port = 3004
    stream_acqui()






