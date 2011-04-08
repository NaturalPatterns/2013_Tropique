#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
    Script de test de la Kinect pour extraire la position 3D
    
"""
# paramètres variables #
verbose=True
depth_min, depth_max= 0., 4.5
N_frame = 100 # time to learn the depth map
tilt = 0 # vertical tilt of the kinect
N_hist = 2**8 
threshold = .08 #3.5
downscale = 4
smoothing = 1.5
noise_level = .8
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
import freenect
import signal
#import frame_convert
from calibkinect import depth2xyzuv, xyz_matrix
import os
import numpy as np
depth_hist = np.load(matname)    
import scipy.ndimage as nd
import socket
#################################################
from position import depth
def display_depth(dev, data, timestamp, verbose=verbose):
    """
    
    Args:
    index: Kinect device index (default: 0)
    format: Depth format (default: DEPTH_11BIT)
    
    Returns:
    (depth, timestamp) or None on error
    depth: A numpy array, shape:(640,480) dtype:np.uint16
    timestamp: int representing the time

    """
    global depth_hist, addrs, prof_m
    Z = depth(data)
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

    for addr in addrs:
        s.sendto(str(prof_m),addr)
        if verbose: print ("datasend = ", prof_m, addr)
 

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
    global depth_hist, record_list, record, addrs, s
    #description res
    hosts = ['127.0.0.1'] #['192.168.1.4', '192.168.1.3']
    port = 3002
    s= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    addrs = [(host,port) for host in hosts]
    print addrs
    
    print('Press Ctrl-C in terminal to stop')
    signal.signal(signal.SIGINT, handler)
    freenect.runloop(depth=display_depth,
                     body=body)
    s.close()

if __name__ == "__main__":
    main()


