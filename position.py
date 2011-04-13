#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
    Script de test de la Kinect pour extraire la position 3D
    
    À partir de la segmentation (cf segmentation.py), on extrait la position 
    (x, y, z) (en fait profondeur, azimuth, élévation) comme le centre de 
    gravité du nuage de points segmentés.    
    
./fake.sh /Users/lup/Desktop/Tropique/dumps/lolo-brume ./position.py






"""
# paramètres variables #
display=True
depth_min, depth_max= 0., 6.
tilt = 0 # vertical tilt of the kinect
N_hist = 2**8 
threshold = .1 #3.5
downscale = 4
smoothing = 1.5
noise_level = .8
figsize=(10,7)
record  = '11-04-13_testing-position.mpg' # None #
if not(display): record = None
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
if display:
    import pylab
    pylab.rcParams.update({'backend': 'Agg'})
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    #import pylab
    plt.ion()
import scipy.ndimage as nd
#################################################
def depth(data):
    """

    """
#    print timestamp
    # from http://nicolas.burrus.name/index.php/Research/KinectCalibration
    Z = 1.0 / (data[::downscale,::downscale] * -0.0030711016 + 3.3309495161)
    shadows = Z > depth_max # irrelevant calculations
    shadows += Z < depth_min # irrelevant calculations
    Z = Z * (1-shadows) + depth_max * shadows
    Z = nd.gaussian_filter(Z, smoothing)
    return Z
    
def display_depth(dev, data, timestamp, display=display):
    """
    
    Args:
    index: Kinect device index (default: 0)
    format: Depth format (default: DEPTH_11BIT)
    
    Returns:
    (depth, timestamp) or None on error
    depth: A numpy array, shape:(640,480) dtype:np.uint16
    timestamp: int representing the time

    """
    global image_depth, i_frame, depth_hist, record_list, ax
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
    
        prof, az, el = -xyz[:,2], -xyz[:,1], -xyz[:,0]
        prof_m, az_m, el_m = prof.mean(), az.mean(), el.mean()

    if display:
        fig = plt.figure(1, figsize=figsize)
#            plt.gray()
        if True: # image_depth:
            ax = fig.add_subplot(111, projection='3d' , animated=True)#
            if detect: 
                image_depth = ax.plot(prof, az, el, 'r.')
                ax.plot([prof_m], [az_m], [el_m], 'go')
            plt.axis('off')
#            cbar = fig.colorbar(image_depth,shrink=0.9,extend='both')
            ax.set_xlabel('prof')
            ax.set_xlim3d(0, depth_max)
            ax.set_ylabel('az')
            ax.set_ylim3d(-2, 2)
            ax.set_zlabel('el')
            ax.set_zlim3d(-1, 1)
            plt.draw()
#        else:
##            image_depth.set_data(attention)
#            image_depth = ax.plot(-xyz[:,2], -xyz[:,0], -xyz[:,1], 'r.')
#            plt.draw()

        if not(record == None):
            figname = record + '_frame%03d.png' % i_frame
            print figname
            fig.savefig(figname, dpi = 72)
            record_list.append(figname)
        plt.close()

    i_frame += 1
    

def handler(signum, frame):
    global keep_running
    keep_running = False

def body(dev, ctx):#*args):
    global keep_running
#    global image_depth
    
    freenect.set_led(dev, 0)
    freenect.set_tilt_degs(dev, tilt)

#    if i_frame > N_frame: keep_running = False

    if not keep_running:
        freenect.set_led(dev, 5)
        raise freenect.Kill

def main():
    global depth_hist, record_list, record
    depth_hist = np.load(matname)    

    print('Press Ctrl-C in terminal to stop')
    signal.signal(signal.SIGINT, handler)
    freenect.runloop(depth=display_depth,
                     body=body)    
    if record:
        os.system('ffmpeg -v 0 -y  -f image2  -sameq -i ' + record + '_frame%03d.png  ' + record + ' 2>/dev/null')
        for fname in record_list: os.remove(fname)

if __name__ == "__main__":
    main()

