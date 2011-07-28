#!/usr/bin/env python
# -*- coding: utf8 -*-

import freenect
import cv
import frame_convert
import numpy as np
import cvblob as cvb
from socket import *
import os
import sys
#from calibkinect import depth2xyzuv, xyz_matrix


depth_min, depth_max= 0., 10.
tilt = 0 # vertical tilt of the kinect
N_hist = 2**8 
threshold1 = .1 #3.5
downscale = 1
smoothing = 1.5
noise_level = .8
figsize=(10,7)


# paramètres fixes #
depth_shape=(640,480)
matname = 'depth_map.npy'
i_frame = 0
record_list = []
image_depth = None
keep_running = True
start = True


threshold = 500
current_depth = 501

global num_detect
num_detect = 0
comp = 0
form = 0

############
try :
    depth_hist = np.load(matname)    
    learn = False
except:
    learn = True
#    depth_hist = np.zeros((depth_shape[0], depth_shape[1], N_hist))
    depth_hist = np.zeros((depth_shape[1]/downscale, depth_shape[0]/downscale, 2))
#depth_hist = np.zeros((depth_shape[1], depth_shape[0], 2)) + 1e-10
#############




def change_threshold(value):
    global threshold
    threshold = value


def change_depth(value):
    global current_depth
    current_depth = value


def array2cv(a):
  dtype2depth = {
        'uint8':   cv.IPL_DEPTH_8U,
        'int8':    cv.IPL_DEPTH_8S,
        'uint16':  cv.IPL_DEPTH_16U,
        'int16':   cv.IPL_DEPTH_16S,
        'int32':   cv.IPL_DEPTH_32S,
        'float32': cv.IPL_DEPTH_32F,
        'float64': cv.IPL_DEPTH_64F,
    }
  try:
    nChannels = a.shape[2]
  except:
    nChannels = 1
  cv_im = cv.CreateImageHeader((a.shape[1],a.shape[0]),
          dtype2depth[str(a.dtype)],
          nChannels)
  cv.SetData(cv_im, a.tostring(),
             a.dtype.itemsize*nChannels*a.shape[1])
  return cv_im



from position import depth

def segm():
	global image_depth, i_frame, depth_hist, learn, record_list
	for i in range (200):
		my_depth, timestamp = freenect.sync_get_depth()
		first_depth = my_depth
		data = my_depth

    		Z = depth(data)
        
        	depth_hist[:, :, 0] = (1-1./(i_frame+1))* depth_hist[:, :, 0] + 1./(i_frame+1) * Z

	np.save(matname, depth_hist) 


def show_depth():
	global threshold
	global current_depth
	player = 0

	my_depth, timestamp = freenect.sync_get_depth()
	first_depth = my_depth

	global image_depth, i_frame, depth_hist, learn, record_list
	
	# from http://nicolas.burrus.name/index.php/Research/KinectCalibration
	data = my_depth
	Z = depth(data)
        score = 1. - Z  / depth_hist[:, :, 0]# ((1.-noise_level)*np.sqrt(depth_hist[:, :, 1]) + noise_level*np.sqrt(depth_hist[:, :, 1]).mean())
	
	my_array= score * (score<threshold1) + (score>threshold1)
	my_array2 = 255 * np.logical_and(my_array >= current_depth - threshold,my_array <= current_depth + threshold)
	my_array2 = my_array2.astype(np.uint8)

	image = array2cv(my_array2)

	font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8) #Creates a font
	cv.PutText(image,"TROPIC", (5,20),font, 255) #Draw the text
	grey = image
	
	img = frame_convert.video_cv(freenect.sync_get_video()[0])

	IPL_DEPTH_LABEL = 32
	labelImg = cv.CreateImage(cv.GetSize(grey), IPL_DEPTH_LABEL, 1)

	blobs = cvb.CvBlobs()
	result = cvb.cvLabel(grey,labelImg,blobs)

	cv.Zero(imgOut);
	cvb.cvRenderBlobs(labelImg, blobs, img, imgOut);
	num_detect = 0
	# Render contours:
	String = str("0")
	detect = 0
	for label, blob in blobs.iteritems(): 
		polygon = cvb.cvConvertChainCodesToPolygon(blob.contour)
		sPolygon = cvb.cvSimplifyPolygon(polygon, 10.)
		area = cvb.cvContourPolygonArea(sPolygon)
		if area>5000 : 
			player += 1

			meanColor = cvb.cvBlobMeanColor(blob, labelImg, img)
			#print "Mean color: r=" + str(meanColor[0]) + ", g=" + str(meanColor[1]) + ", b=" + str(meanColor[2])
			centr = cvb.cvCentroid(blob)
			#print (int(centr[0]),int(centr[1]))
			dist = first_depth[int(centr[1])][int(centr[0])]
			
			cPolygon = cvb.cvPolygonContourConvexHull(sPolygon)
	     	
			cvb.cvRenderContourChainCode(blob.contour, imgOut)
			cvb.cvRenderContourPolygon(sPolygon, imgOut,cv.CV_RGB(0, 0, 255))
			cvb.cvRenderContourPolygon(cPolygon, imgOut,cv.CV_RGB(0, 255, 0))
	
			# Render internal contours:
			for contour in blob.internalContours: 
				cvb.cvRenderContourChainCode(contour, imgOut)

			String= ((str(int(player))+ " " + str(int(centr[0])) + " " + str(int(centr[1])) +" "+ str(int(dist)) + " ; \n"))	
	try :	
		Donnee, Client = PySocket.recvfrom (1024)
		print Donnee
	except:
		detect = 0
	else :
		if Donnee == "data":
			PySocket.sendto (String,Client)
			print timestamp
		if Donnee == "segm":
			print "segm load... wait!"
			try :	
				os.system('rm depth_map.npy')
			except :
				print "no depth_map.npy found"

			try: 
				segm()
			except :
				print "segmentation fault :)"
				String ="fault"
				PySocket.sendto (String,Client)
				print "segmentation fault" 
			else :
				String ="ok"
				PySocket.sendto (String,Client)
				print "segmentation ok" 
		if Donnee == "kill":
			sys.exit (0)


			#os.system('python segmentation.py')
	#comp = comp + 1





	cv.ShowImage('Depth', imgOut)


def show_video():
    cv.ShowImage('Video', frame_convert.video_cv(freenect.sync_get_video()[0]))


cv.NamedWindow('Depth')
cv.NamedWindow('Video')


print('Press ESC in window to stop')

imgOut = cv.CreateImage((640,480), cv.IPL_DEPTH_8U,3)

PySocket = socket (AF_INET,SOCK_DGRAM)
PySocket.bind (('192.168.1.103',9999))
PySocket.settimeout(0.001)

while 1:
    show_depth()
    show_video()
    if cv.WaitKey(10) == 27:
        break
