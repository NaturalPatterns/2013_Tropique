#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
    Script de test de la Kinect pour extraire la position 3D

    Avec le script position.py, on a extrait le centre de gravité. 
    On envoie maintenant cette position au réseau pour reception dans les scripts live_*.py

    Ce script définit la kinect comme serveur

./fake.sh /Users/lup/Desktop/Tropique/dumps/lolo-brume ./send_position.py
    
Mercurial is really a cool stuff



"""
# paramètres variables #
verbose = True # False #
depth_min, depth_max= 0., 6.
tilt = 0 # vertical tilt of the kinect
N_hist = 2**8 
threshold = .1 #
downscale = 4
smoothing = 1.5
noise_level = .8
emulate = False # True # 
host = 'localhost' # '127.0.0.1' #localhost['192.168.1.4', '192.168.1.3']
port = 50042
buf = 1024
# paramètres fixes #
depth_shape=(640,480)
matname = 'depth_map.npy'
i_frame = 0
record_list = []
image_depth = None
keep_running = True
start = True
prof_m, az_m, el_m = depth_max, 0. , 0.
#################################################
import numpy as np
from calibkinect import depth2xyzuv#, xyz_matrix
if not(emulate): 
    import freenect
    from position import depth
    depth_hist = np.load(matname)    
else:
    depth_hist = np.ones((depth_shape[0]/downscale,depth_shape[1]/downscale,2)) * depth_max
    def depth(data):
        return data[::downscale,::downscale]
import time
import signal
#import frame_convert
#import os
#import scipy.ndimage as nd
import socket
# we define the server
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket.SOCK_DGRAM) #
#    addrs = [(host, port) for host in hosts]
#    print addrs
addr = (host,port)
s.bind(addr)
#s.settimeout(500) # time-out for establishing the connection
s.listen(1) # how many clients can connect to this server
print 'Waiting for a connection from a client on ', addr
conn, addr_ = s.accept() # waits until a clients connects
print 'Connected by', addr_
#################################################
def display_depth(dev, data, timestamp, verbose=verbose):
    """
    
    Args:

    
    Returns:

    """
    global depth_hist, s, conn
    Z = depth(data)
#    print data.shape, Z.shape, depth_hist.shape
#    score = (depth_hist[:, :, 0] - Z)  / ((1.-noise_level)*np.sqrt(depth_hist[:, :, 1]) + noise_level*np.sqrt(depth_hist[:, :, 1]).mean())
    score = 1. - Z  / depth_hist[:, :, 0]# ((1.-noise_level)*np.sqrt(depth_hist[:, :, 1]) + noise_level*np.sqrt(depth_hist[:, :, 1]).mean())
    attention = np.argwhere(score.ravel() > threshold)
    detect =  (attention.shape[0] > 0)
    if detect:
        # computing positions
        U, V = np.mgrid[:480:downscale,:640:downscale]
        U_, V_ = U.ravel(), V.ravel()
        data_ = data[::downscale,::downscale].ravel()
        xyz, uv = depth2xyzuv(data_[attention], u=U_[attention], v=V_[attention])
    
        prof, az, el = -xyz[:,2], -xyz[:,0], -xyz[:,1]
        prof_m, az_m, el_m = prof.mean(), az.mean(), el.mean()
    else:
        prof_m, az_m, el_m = depth_max, depth_max, depth_max

    data = conn.recv(buf)
    if data == 'ready': 
        print('data received is ', data)
#    for addr in addrs:
    #dat = s.recvfrom(buf)
#    if True:#dat == 'ask':
        #        s.sendto(str(prof_m),addr)
#        if verbose: print ("datasend = ", prof_m, addr)
        my_array = str(prof_m) + "," + str( az_m) +"," + str( el_m) + '\n \r'
#        s.sendto((my_array),(host, port))
        conn.send(my_array)
        if verbose: print ("datasend = ", my_array , (host, port))
#    time.sleep(0.1)
    elif data == 'done':
        keep_running = False
        pass
    else:
        print('nobody asks for something... is the client dead?')

def handler(signum, frame):
    global keep_running
    keep_running = False

def body(dev, ctx):#*args):
    global keep_running
#    global image_depth
    
    freenect.set_led(dev, 0)
    freenect.set_tilt_degs(dev, tilt)


    if not keep_running:
        freenect.set_led(dev, 5)
        raise freenect.Kill

def main():
    global depth_hist, s, conn
    #description res

    
    print('Press Ctrl-C in terminal to stop')
    signal.signal(signal.SIGINT, handler)
    if not(emulate):
        freenect.runloop(depth=display_depth,
                     body=body)
    else:
        dev, timestamp = None, None
        pos = np.ones(depth_shape) * depth_max
        pos[pos.shape[0]/2, pos.shape[1]/2] = depth_max/2.
        while True:
            #    time.sleep(0.1)
            display_depth(dev, pos, timestamp, verbose=verbose)

    conn.close()
    s.close()

if __name__ == "__main__":
    main()
