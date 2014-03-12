#!/usr/bin/env python
# -*- coding: utf8 -*-
""" le client centralise  l'ensemble des commandes a envoyé au différents serveur kinect difini dans myarc
"""
import sys
sys.path.append('..')
from parametres import info_kinects, DEBUG
import socket
import os
nbr_kinect = 0
import time as time
from threading import Thread
global f
global matrix
matrix = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#DEBUG=True

class testkin(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.status = -1
        self.HOST = '10.42.0.20'
        self.port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto('data', (self.ip, self.port))
        sock.settimeout(0.5)
        try:
            received = sock.recv(512)
#        except KeyboardInterrupt:
#            print "stop acquisition kinect"
        except:
            print "PROBLEME no data in ", self.ip, self.port
#            matrix[int(self.ip[8:]) - 10] += 1
##            print "matrix =", matrix
#            if matrix[int(self.ip[8:]) - 10] > 10000:
#                print "send reboot to ", self.ip
#                matrix[int(self.ip[8:]) - 10] = 0
#                sock.sendto('boot', (self.ip, self.port))
            self.status = 0
        else:
            if (DEBUG and received != ""):
                print "received = ", received, " from ", self.ip, self.port
            if (DEBUG and received == ""):
                print "received 0", " from ", self.ip, self.port
            self.status = received


def list_kinect():
    os.system('clear')
    print "\n \t liste des kinects dans architecture \n"
    print "il y a ", (len(info_kinects)), " kinects configuré \n"
    for ligne in range(len(info_kinects)):
        print ligne, info_kinects[ligne]


def stream_acqui():
#    os.system('clear')
    print "listen to kinects server "
    teston = 0
    last_time = 0
    goodsend = 0

    while (teston < 1):
#        a = time.time()
#        b = a - last_time
#        print "the time lapsed = ",b , 1/float(b)
#        last_time = a
        serverkinects = []
        for kin in info_kinects:
            ip = kin['address']
            port = kin['port']
            current = testkin(ip, 9998+port)
            serverkinects.append(current)
            current.start()
        all_pos = ""
        for server in serverkinects:
            server.join()
            try:
                var = int(server.status)
            except:
                all_pos += server.status
            else:
                pass
        all_pos = all_pos[0:(len(all_pos) - 1)]
        try:
            sendor, Client = sock_confirm.recvfrom(1024)
        except (KeyboardInterrupt):
            print "break demande"
#            break
#            raise
        except:
            pass
        else:
            goodsend = 1

        if (goodsend == 1 and all_pos != ""):
#            print "send  =", all_pos
            sock_to_affi.sendto((all_pos), (affi_host, affi_port))
            goodsend = 0


def segment():
    os.system('clear')
    print "calibration"
    for kin in info_kinects:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print "send calibration to ", kin['address'], kin['port'], kin['max']
        HOST = kin['address']
        PORT = 9998 + kin['port']
        sock.sendto("init " + str(kin['max']), (HOST, PORT))
        time.sleep(1)
    time.sleep(20)
    print "end calibration "

if __name__ == "__main__":
    os.system('clear')
    # SOCK_DGRAM is the socket type to use for UDP sockets
    sock_to_affi = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    sock_pd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    affi_host = 'localhost'
    affi_port = 3004
    sock_confirm = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_confirm.bind(("127.0.0.1", 5555))
    sock_confirm.setblocking(0)
    list_kinect()
    print "send to ",affi_host, affi_port
    print "calibration des kinects"
    segment()

    stream_acqui()

    while 1 :
        print "\n \t \t client.py = CLIENT KINECTS  in TROPIC \n"
        print "0 - stop prog"
        print "1 - liste des kinects"
        print "..."
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
