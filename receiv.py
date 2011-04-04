import socket
#print socket.__version__
#description res
host = '192.168.1.4'
port = 3002
buf = 1024

b= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
addr =(host,port)
print addr
b.bind(addr)
b.settimeout(5)

while 1:
	try :
		dat = b.recvfrom(1024)
	except:
		print ("nodata")
	else :
		print float(dat[0])
