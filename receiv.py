import socket
import signal, sys
#print socket.__version__
#description res
host = '127.0.0.1'#192.168.1.4'
port = 3002
buf = 1024

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
addr =(host,port)
print addr
s.bind(addr)
s.settimeout(5)

def handler(signum, frame):
    s.close()
    sys.exit()

def main():
    print('Press Ctrl-C in terminal to stop')
    signal.signal(signal.SIGINT, handler)
    while 1:
	try :
		dat = s.recvfrom(1024)
	except:
		print ("nodata")
	else :
		print float(dat[0])

    
if __name__ == "__main__":
    main()

