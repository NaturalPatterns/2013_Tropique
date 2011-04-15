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

global prof_m , az_m , el_m


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
		dat_brut=str(dat[0])
		datasplit1 = dat_brut.split(",")
		prof_m =  float(datasplit1[0])
		datasplit2 = datasplit1[1].split(",")
		az_m =  float (datasplit2[0])
		el_m = float(datasplit1[2])
		print ("receiv = ", prof_m, az_m , el_m)			


    
if __name__ == "__main__":
    main()

