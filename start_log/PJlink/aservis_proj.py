# -*- coding: utf-8 -*-
"""
Created on Thu May 24 11:32:24 2012

@author: tropic
"""

# Echo client program
import socket
import hashlib
import hashlib
import sys
import telnetlib
import socket
import re
from Ping import *
global PJLINK_TIMEOUT , PJLINK_PORT , PJLINK_DEBUG
# Timeout lors du ping ( en s )
PJLINK_TIMEOUT=0.1

# Port utilisé par le PJLINK
PJLINK_PORT=4352

# Debug mode :  0 => pas de debug, 1 => debug simple, 2 => debug verbeux
PJLINK_DEBUG = 1

import socket

from_IP="localhost"
from_PORT=30001
from_send = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP
from_send.bind(("", from_PORT))

class PjLinkError(Exception):
	def __init__(self,value,desc):
		self.value = value
		self.desc = desc
	def __str__(self):
		return repr(str(self.value) + " " + str(self.desc))
  
def run_command(ip,passwd,cmd):
    tn = None
    try:
        tn = telnetlib.Telnet(ip,PJLINK_PORT)
        if PJLINK_DEBUG and PJLINK_DEBUG > 1:
            tn.set_debuglevel(1000)
        res = tn.read_until("\r",1)
        if "1" in res:
            if PJLINK_DEBUG > 0 :
                print "Connexion securisee ...."
            res = res[9:17]
            pjlink_mode = 1
        elif "0" in res:
            if PJLINK_DEBUG > 0 :
                print "Connexion NON securisee ...."
            pjlink_mode = 0
        else:
            # Erreur inconnue
            raise PjLinkError("UNK_MODE", "Mode PJLink Inconnu")
            return int(-1)
        if (pjlink_mode == 1):
            # PJLINK sécurisé - il faut générer le md5 qui va bien
            tn.write(str(gen_md5(str(passwd),res)) + str(cmd) + "\r")
        else:
            # PJLINK non sécurisé - on envoie la commande directement
            tn.write(str(cmd) + "\r")
        result = tn.read_until("\r",5)
        print result
        # On quite proprement la connexion telnet
        tn.close()
    # On traite les différentes exceptions possibles
    except EOFError, e:
        raise PjLinkError("CON_FAIL", "EOF Error")
        return int(-1)
    except socket.gaierror, e:
        raise PjLinkError("CON_FAIL", "Socket GAIERROR" + e[1])
    except socket.error :
        if tn:
            tn.close()
        print("CON_FAIL", "Socket Error")
        if PJLINK_DEBUG > 0 :
            print "Could not open socket: "# + message
        return int(-1)
    return result
 
# Fonction générant le hash md5 corespondant a la norme PJLINK
def gen_md5(passwd,random_seq):
	msg = str(random_seq) + str(passwd)
	h = hashlib.md5()
	h.update(msg)
	return h.hexdigest()
 

while  True :
    Donnee, Client = from_send.recvfrom (512)
    print Donnee
    
    ip = "10.42.0.15" + Donnee[2]
    print "ip cible =",ip    # The remote host
    PORT = 4352              # The same port as used by the server
    passwd = "TROPIC"
    cmd = str("%1POWR ")+Donnee[0] + "\r"
    print "commande =", cmd
    run_command(ip,passwd,cmd)






