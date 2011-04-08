import socket
import signal, sys, time
#print socket.__version__
#description res
host = '127.0.0.1' # 192.168.1.4'
port = 30002
buf = 1024

s = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM) # socket.SOCK_STREAM) # 
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
    while True:
        try :
             dat = s.recvfrom(buf)
        except:
             print ("nodata")
        else :
             dat_brut=str(dat[0])
             print dat
             datasplit1 = dat_brut.split(",")
             prof_m =  float(datasplit1[0])
             datasplit2 = datasplit1[1].split(",")
             az_m =  float (datasplit2[0])
             el_m = float(datasplit1[2])
             print ("receiv = ", prof_m, az_m , el_m)
    time.sleep(1.)
    
if __name__ == "__main__":
    main()

