#!/usr/bin/env python
# -*- coding: utf8 -*-

# paramètres variables #
display=True
depth_min, depth_max= 0., 10.
tilt = 0 # vertical tilt of the kinect
N_hist = 2**8 
threshold = .1 #3.5
downscale = 4
smoothing = 1.5
noise_level = .8
figsize=(10,7)
N_frame = 200 # maximum time to learn the depth map
record  = '11-04-13_testing-segmentation.mpg' # None #
if not(display): record = None
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



















import freenect
import cv
import frame_convert


try :
    depth_hist = np.load(matname)    
    learn = False
except:
    learn = True
#    depth_hist = np.zeros((depth_shape[0], depth_shape[1], N_hist))
    depth_hist = np.zeros((depth_shape[1]/downscale, depth_shape[0]/downscale, 2))
#depth_hist = np.zeros((depth_shape[1], depth_shape[0], 2)) + 1e-10

#def gaussian(x, m, var):
#    return 1./np.sqrt(2.*np.pi)/np.sqrt(var)*np.exp(-.5*(x-m)**2/var)

from position import depth

keep_running = True





from position import depth
def display_depth(dev, data, timestamp, display=display):
    
    global image_depth, i_frame, depth_hist, learn, record_list
#    print timestamp
    # from http://nicolas.burrus.name/index.php/Research/KinectCalibration
    Z = depth(data)

    global keep_running
    
    print type((data))

    #        data = pretty_depth(data)
    #        proba = gaussian(data, depth_hist[:, :, 0], depth_hist[:, :, 1])
    ##        smoothed = ndimage.gaussian(np.log(proba), 5.)
    #        print np.log(proba).min(), np.log(proba).max()
    #        score = (depth_hist[:, :, 0] - Z)  / depth_hist[:, :, 0]# ((1.-noise_level)*np.sqrt(depth_hist[:, :, 1]) + noise_level*np.sqrt(depth_hist[:, :, 1]).mean())
    score = 1. - Z  / depth_hist[:, :, 0]# ((1.-noise_level)*np.sqrt(depth_hist[:, :, 1]) + noise_level*np.sqrt(depth_hist[:, :, 1]).mean())
        
    print i_frame, score.min(), score.max()
#        score = 1. / (1 + np.exp(-(score-threshold)/1.))
    #print (score * (score<threshold) + (score>threshold))
    return_img = (score * (score<threshold) + (score>threshold)) 
    print return_img ,data.shape, depth_hist[:, :, 0].shape
    cv.ShowImage('Depth', frame_convert.pretty_depth_cv(data))


    if cv.WaitKey(10) == 27:
        keep_running = False


def display_rgb(dev, data, timestamp):
    global keep_running
    cv.ShowImage('RGB', frame_convert.video_cv(data))
    if cv.WaitKey(10) == 27:
        keep_running = False


def body(*args):
    if not keep_running:
        raise freenect.Kill


def handler(signum, frame):
    global keep_running
    keep_running = False



def main():

    global depth_hist, record_list, record
    print('Press Ctrl-C in terminal to stop')
    signal.signal(signal.SIGINT, handler)
    freenect.runloop(depth=display_depth,video=display_rgb,
                     body=body)


 

    if learn == True:
        np.save(matname, depth_hist) 
        
    if record:
        os.system('ffmpeg -v 0 -y  -f image2  -sameq -i  ' + record + '_frame%03d.png  ' + record + ' 2>/dev/null')
        for fname in record_list: os.remove(fname)

 
if __name__ == "__main__":

    cv.NamedWindow('Depth')
    cv.NamedWindow('RGB')
    main()
