#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
    Script de test de la Kinect pour extraire la position 3D
    
    Segmentation basé sur une captation sans personne

./fake.sh /Users/lup/Desktop/Tropique/dumps/rien ./segmentation.py 

    Il faut recommencer la segmentation dès qu'on change le point de vue de la Kinect.
    Pour recommencer une segmentation supprimemer le fichier matname:
        rm depth_map.npy

    Pour tester la valeur de score, relancer le programme sur une scene avec une personne:
./fake.sh /Users/lup/Desktop/Tropique/dumps/lolo-brume ./segmentation.py 
HOHOHO
"""
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

comp = 0

threshold = 250
current_depth = 720
global num_detect
num_detect = 0


#################################################

import freenect
import signal
#import frame_convert
from calibkinect import depth2xyzuv, xyz_matrix
import os
import numpy as np
'''if display:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    #import pylab
    plt.ion()
'''
#import scipy.ndimage as nd
import cv
import frame_convert
import cvblob as cvb

#################################################

cv.NamedWindow('juju',1)
imgOut = cv.CreateImage((640,480), cv.IPL_DEPTH_8U,3)
img = cv.LoadImage("test.png",1)
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

#from position import depth

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

    cv.ShowImage('Depth', frame_convert.pretty_depth_cv(data))

    imgOut = frame_convert.pretty_depth_cv(data)

    cv.ShowImage('juju', img)
    #show_blob()
    print data

    '''

    global image_depth, i_frame, depth_hist, learn, record_list
#    print timestamp
    # from http://nicolas.burrus.name/index.php/Research/KinectCalibration
    Z = depth(data)

    if learn :
#        data = pretty_depth(data) # on 8-bits
#        data = data / 255. #data.max()
        
#        xyz, uv = depth2xyzuv(data)
##        print xyz.shape, uv.shape
#        data = xyz[:,2].reshape((480,640))
#        data = data * (data >0)
        print i_frame, Z.shape, Z.min(), Z.max()
#        print timestamp, i_frame, Z.shape, depth_hist.shape

        
        depth_hist[:, :, 0] = (1-1./(i_frame+1))* depth_hist[:, :, 0] + 1./(i_frame+1) * Z
#        if i_frame>0:
#            depth_hist[:, :, 1] = (1-1./(i_frame))* depth_hist[:, :, 1] + 1./i_frame * (Z-depth_hist[:, :, 0])**2
        
#        print np.log(depth_hist[:, :, 1]).min(), np.log(depth_hist[:, :, 1]).max()
        if display:
#            plt.gray()
            plt.figure(1, figsize=figsize)
            if image_depth:
                image_depth.set_data(depth_hist[:, :, 0])
#                image_depth.set_alpha(depth_hist[:, :, 1]/depth_hist[:, :, 1].max())
            else:
                image_depth = plt.imshow(depth_hist[:, :, 0], interpolation='nearest', animated=True, vmin=0, vmax=depth_max)
                plt.axis('off')
                plt.colorbar() 
            plt.draw()        
    else:
#        data = pretty_depth(data)
#        proba = gaussian(data, depth_hist[:, :, 0], depth_hist[:, :, 1])
##        smoothed = ndimage.gaussian(np.log(proba), 5.)
#        print np.log(proba).min(), np.log(proba).max()
#        score = (depth_hist[:, :, 0] - Z)  / depth_hist[:, :, 0]# ((1.-noise_level)*np.sqrt(depth_hist[:, :, 1]) + noise_level*np.sqrt(depth_hist[:, :, 1]).mean())
        score = 1. - Z  / depth_hist[:, :, 0]# ((1.-noise_level)*np.sqrt(depth_hist[:, :, 1]) + noise_level*np.sqrt(depth_hist[:, :, 1]).mean())
        
        print i_frame, score.min(), score.max()
#        score = 1. / (1 + np.exp(-(score-threshold)/1.))
        if display:
#            plt.gray()
            fig = plt.figure(1, figsize=figsize)
            if image_depth:
                image_depth.set_data(score * (score<threshold) + (score>threshold))
            else:
                image_depth = plt.imshow(score * (score<threshold) + (score>threshold), interpolation='nearest', animated=True, vmin=0, vmax=1.)
                plt.axis('off')
                plt.colorbar()        
            plt.draw()

    if not(record == None):
        figname = record + '_frame%03d.png' % i_frame
        plt.savefig(figname, dpi = 72)
        record_list.append(figname)
    i_frame += 1
    '''    
def handler(signum, frame):
    global keep_running
    keep_running = False

#def display_rgb(dev, data, timestamp):
#    global keep_running
#    cv.ShowImage('RGB', frame_convert.video_cv(data))
#    if cv.WaitKey(10) == 27:
#        keep_running = False

def body(dev, ctx):#*args):
    global keep_running, tilt
    
    freenect.set_led(dev, 0)
    freenect.set_tilt_degs(dev, tilt)

    if i_frame > N_frame: keep_running = False

    if not keep_running:
        freenect.set_led(dev, 5)
        raise freenect.Kill    

   
def main():
    #comp= comp + 1
    cv.NamedWindow('Depth',1)

    global depth_hist, record_list, record
    print('Press Ctrl-C in terminal to stop')
    signal.signal(signal.SIGINT, handler)
    freenect.runloop(depth=display_depth, body=body)
    

    if learn == True:
        np.save(matname, depth_hist) 
        
    if record:
        os.system('ffmpeg -v 0 -y  -f image2  -sameq -i  ' + record + '_frame%03d.png  ' + record + ' 2>/dev/null')
        for fname in record_list: os.remove(fname)

if __name__ == "__main__":
    main()

#    see https://gist.github.com/717060
#    freenect.runloop(lambda *x: depth_callback(*freenect.depth_cb_np(*x)))
#    
#    def depth_callback(dev, data, timestamp):
#        
#        """libfreenect will call this func once per frame"""
#
#        global lock
#        global notes_on
#
#        lock.acquire()
#        # do some computing
#
#        lock.release()
#
