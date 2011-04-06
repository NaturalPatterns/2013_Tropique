#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
    Script de test de la Kinect pour extraire la position 3D
    
"""
# paramètres variables #
display=True
record  = 'position.mpg' # None #
depth_min, depth_max= 0., 4.5
N_frame = 100 # time to learn the depth map
tilt = 0 # vertical tilt of the kinect
N_hist = 2**8 
threshold = 5.
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
#################################################
import freenect
import signal
#import frame_convert
from calibkinect import depth2xyzuv, xyz_matrix
import os
import numpy as np
depth_hist = np.load(matname)    
if display:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    #import pylab
    plt.ion()
import scipy.ndimage as nd
import socket
#################################################

def display_depth(dev, data, timestamp, display=False):
    """
    
    Args:
    index: Kinect device index (default: 0)
    format: Depth format (default: DEPTH_11BIT)
    
    Returns:
    (depth, timestamp) or None on error
    depth: A numpy array, shape:(640,480) dtype:np.uint16
    timestamp: int representing the time

    """
    global image_depth, i_frame, depth_hist, addrs, s
    # low-level segmentation
    # from http://nicolas.burrus.name/index.php/Research/KinectCalibration
    Z = 1.0 / (data * -0.0030711016 + 3.3309495161)
    shadows = Z > depth_max # irrelevant calculations
    shadows += Z < depth_min # irrelevant calculations
    Z = Z * (1-shadows) + depth_max * shadows
    score = (depth_hist[:, :, 0] - Z) / (np.sqrt(depth_hist[:, :, 1]) + .5*np.sqrt(depth_hist[:, :, 1]).mean()) 
    score = score * (1-shadows)  - 10. * shadows
    ROI = score > 0.
    #print Z.mean()
    if np.sum(ROI) > 0:
        Z_mean = np.sum(Z*ROI) / np.sum(ROI)    
        print Z_mean
        for addr in adrrs:
            s.sendto(str(Z_mean),addr)
            print ("datasend = ", Z_mean, addr)
        
def handler(signum, frame):
    global keep_running
    keep_running = False

def body(*args):
    if not keep_running:
        raise freenect.Kill    
    
def main():
    global depth_hist, record_list, record, addrs, s
    #description res
    host = ['192.168.1.4', '192.168.1.3']
    port = 3002
    s= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    addrs = [(host,port) for host in hosts]
    print addrs
    
    
    print('Press Ctrl-C in terminal to stop')
    signal.signal(signal.SIGINT, handler)
    freenect.runloop(depth=display_depth,
                     body=body)
    
    if record:
        os.system('ffmpeg -v 0 -y  -f image2  -sameq -i _frame%03d.png  ' + record + ' 2>/dev/null')
        for fname in record_list: os.remove(fname)



if __name__ == "__main__":
    main()

