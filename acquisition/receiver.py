# Server program

from socket import *

# Set the socket parameters
host = "localhost"
port = 21567
buf = 1024
addr = (host,port)

# Create socket and bind to address
UDPSock = socket(AF_INET,SOCK_DGRAM)
UDPSock.bind(addr)
UDPSock.settimeout(0.001)

# Receive messages
while 1:
	try :
		data,addr = UDPSock.recvfrom(buf)
	except: 
		ab = 1
		#print "Client has exited!"
			#break
	else:
		print "\nReceived message '", data

# Close socket
UDPSock.close()

