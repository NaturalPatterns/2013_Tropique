#!/usr/bin/env python
# -*- coding: utf8 -*-
""" le client centralise  l'ensemble des commandes a envoyé au différents serveur kinect difini dans myarc
"""

import signal
import socket
import sys
import os
from architecture import kinects
import termios, fcntl, sys, os

nbr_kinect = 0
global teston
teston =0

def list_kinect():
	os.system('clear')
	print "\n \t liste des kinects dans architecture \n"
	
	print "il y a ", (len (kinects)) , " kinects configuré \n",
	for ligne in range (len (kinects)):
		print ligne, kinects[ligne]

def stream_acqui():
	os.system('clear')
	print "listen to kinects server "
	# SOCK_DGRAM is the socket type to use for UDP sockets

	teston =0
	while (teston < 1) :
		String =""
		for kin in kinects :
			#print kin['address'], kin['port']
			HOST = kin['address']
			PORT = kin['port']
			data = " ".join(sys.argv[1:])
			sock.sendto("data" , (HOST, PORT))
			sock.settimeout(1)
			try :
				received = sock.recv(1024)
 			except KeyboardInterrupt:
        			print "stop acquisition kinect"
				teston  = teston + 1
			
			except :
				#print "PROBLEME no data in ", HOST, PORT
        			#print "stop acquisition kinect"
				teston  = teston 
			else :
				try :
					var= int (received)
				except :
					print "from ",HOST," Received: ", received
					String = String + " " +HOST+ "o" +received
		print "send  =", String
		sock_pd.sendto((String ), (host_pd, port_pd))

def segment():
	os.system('clear')
	print "listen to kinects server "	
	for kin in kinects :
		print kin['address'], kin['port']
		HOST = kin['address']
		PORT = kin['port']
		data = " ".join(sys.argv[1:])
		sock.sendto("segm" , (HOST, PORT))
		sock.settimeout(20)
		try :
			received = sock.recv(1024)
		except :
			print "PROBLEME no data in ", HOST, PORT
		else :
			print "Received: %s" % received

def kill_kinect():
	os.system('clear')
	print "try to kill kinects server "
	for kin in kinects :
		print kin['address'], kin['port']
		HOST = kin['address']
		PORT = kin['port']
		data = " ".join(sys.argv[1:])
		sock.sendto("kill" , (HOST, PORT))



if __name__ == "__main__":
	os.system('clear')
	nbr_kinect  =(len (kinects))
	print " nbr kinect = ", nbr_kinect
	# SOCK_DGRAM is the socket type to use for UDP sockets
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_pd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	host_pd = 'localhost'
	port_pd = 3001

	while 1 :
		print "\n \t \t client.py = CLIENT KINECTS  in TROPIC \n"
		print "0 - stop prog"
		print "1 - liste des kinects"
		print "..."
		print "7 - kill/start kinect"
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
			if choice == 7 :
				kill_kinect()
			if choice ==8 :
				segment()
			if choice ==9 :
				stream_acqui()





