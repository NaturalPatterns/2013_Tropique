# -*- coding: utf-8 -*-
"""
Created on Thu May 24 11:32:24 2012

@author: tropic
"""

# Echo client program
import socket
import hashlib

# Fonction générant le hash md5 corespondant a la norme PJLINK
def gen_md5(passwd,random_seq):
	msg = str(random_seq) + str(passwd)
	h = hashlib.md5()
	h.update(msg)
	return h.hexdigest()
 

HOST = "10.42.0.152"    # The remote host
PORT = 4352              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('Hello, world')

data = s.recv(2024)
print 'Received', repr(data)
print 'Received', repr(data[9:17])
passwd = "TROPIC"
s.sendall(str(gen_md5(str(passwd),repr(data[9:17]))) + "%1POWR ?\r")
data = s.recv(2024)
print 'Received', repr(data)
#s.sendall('%1NAME ?\r')
s.close()



