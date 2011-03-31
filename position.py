#!/usr/bin/env python
import freenect
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#import pylab
import signal
#import frame_convert
from calibkinect import depth2xyzuv
import os

plt.ion()
image_depth = None
keep_running = True
record, record_list = 'position.mpg', []

import numpy as np

depth_shape=(640,480)
depth_min, depth_max= 0., 3.5
N_hist = 2**8 
max_depth = 3.5 # in meters
matname = 'depth_map.npy'
depth_hist = np.load(matname)    

i_frame = 0

def display_depth(dev, data, timestamp, display=True):
    """
    
    Args:
    index: Kinect device index (default: 0)
    format: Depth format (default: DEPTH_11BIT)
    
    Returns:
    (depth, timestamp) or None on error
    depth: A numpy array, shape:(640,480) dtype:np.uint16
    timestamp: int representing the time

    """
    global image_depth, i_frame, depth_hist, learn, record_list
    # low-level segmentation
    # from http://nicolas.burrus.name/index.php/Research/KinectCalibration
    Z = 1.0 / (data * -0.0030711016 + 3.3309495161)
    shadows = Z > depth_max # irrelevant calculations
    shadows += Z < depth_min # irrelevant calculations
    Z = Z * (1-shadows) + depth_max * shadows
    score = (depth_hist[:, :, 0] - Z) / (np.sqrt(depth_hist[:, :, 1]) + .5*np.sqrt(depth_hist[:, :, 1]).mean()) 
    attention = np.argwhere(score.ravel() > .4)
    print score.min(), score.max(), score.mean(), attention
    # computing positions
    U, V = np.mgrid[:480,:640]
    U, V = U.ravel(), V.ravel()
    data_ = data.ravel()
    print  V[attention] # data_[attention], U[attention],
    xyz, uv = depth2xyzuv(data[attention], u=U[attention], v=V[attention])
    
    if display:
#            plt.gray()
        fig = plt.figure(1)
        ax = fig.add_subplot(111, projection='3d')# , animated=True
#        if image_depth:
#            image_depth.set_data(attention)
#        else:
        sc = ax.scatter(xyz[:,0], xyz[:,1], xyz[:,2], c='r')
        plt.axis('off')
        cbar = fig.colorbar(sc,shrink=0.9,extend='both')
        plt.draw()

    if not(record == None):
        figname = '_frame%03d.png' % i_frame
        plt.savefig(figname, dpi = 72)
        record_list.append(figname)
    i_frame += 1
    
def handler(signum, frame):
    global keep_running
    keep_running = False

def body(*args):
    if not keep_running:
        raise freenect.Kill    
    
def main():
    global depth_hist, record_list, record
    print('Press Ctrl-C in terminal to stop')
    signal.signal(signal.SIGINT, handler)
    freenect.runloop(depth=display_depth,
                     body=body)
    
    if record:
        os.system('ffmpeg -v 0 -y  -f image2  -sameq -i _frame%03d.png  ' + record + ' 2>/dev/null')
        for fname in record_list: os.remove(fname)

if __name__ == "__main__":
    main()

