# -*- coding: utf-8 -*-

import socket
def Ping(ip,port,timeout):
	ping = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		ping.settimeout(timeout)
		ping.connect((ip,port))
		ping.close()
		return 1
	except socket.error:
		return False
