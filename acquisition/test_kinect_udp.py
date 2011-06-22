# Copyright (C) 2007 by Cristobal Carnero Linan
# grendel.ccl@gmail.com
#
# This file is part of cvBlob.
#
# cvBlob is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cvBlob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public License
# along with cvBlob.  If not, see <http://www.gnu.org/licenses/>.
#

# ----------------------------------------------------------------------------------
# NOTE - zorzalzilba  
# This file is a python version of the original C++ test/test.cpp
# ----------------------------------------------------------------------------------

# Import opencv and cvblob python extensions
# Note: these must be findable on PYTHONPATH
import cv
import cvblob as cvb

#!/usr/bin/env python
import freenect
import cv
import frame_convert
import numpy as np
import socket


threshold = 250
current_depth = 720
global num_detect
num_detect = 0

comp = 0

#!/usr/bin/env python
import freenect
import cv
import frame_convert

"""
#img = cv.LoadImage("test.png",1)
#img = frame_convert.pretty_depth_cv(freenect.sync_get_depth()[0])
cv.SetImageROI(img, (100, 100, 800, 500))

grey = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U,1)
cv.CvtColor(img, grey, cv.CV_BGR2GRAY)
cv.Threshold(grey, grey, 100, 255, cv.CV_THRESH_BINARY)

"""


def change_threshold(value):
    global threshold
    threshold = value


def change_depth(value):
    global current_depth
    current_depth = value


def show_blob(comp):
	player = 0
	depth, timestamp = freenect.sync_get_depth()
	first_depth = depth
	depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
	depth = depth.astype(np.uint8)
    
	#print depth
	font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8) #Creates a font

	image = cv.CreateImageHeader((depth.shape[1], depth.shape[0]),cv.IPL_DEPTH_8U,1)

	cv.SetData(image, depth.tostring(),depth.dtype.itemsize * depth.shape[1])
	cv.PutText(image,"TROPIC", (5,20),font, 255) #Draw the text
	grey = image
	
	img = frame_convert.video_cv(freenect.sync_get_video()[0])

	#print type (img)

	IPL_DEPTH_LABEL = 32
	labelImg = cv.CreateImage(cv.GetSize(grey), IPL_DEPTH_LABEL, 1)

	blobs = cvb.CvBlobs()
	result = cvb.cvLabel(grey,labelImg,blobs)

	#imgOut = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U,3)
	cv.Zero(imgOut);
	cvb.cvRenderBlobs(labelImg, blobs, img, imgOut);
	num_detect = 0
	# Render contours:
	for label, blob in blobs.iteritems(): 
		polygon = cvb.cvConvertChainCodesToPolygon(blob.contour)
		sPolygon = cvb.cvSimplifyPolygon(polygon, 10.)
		area = cvb.cvContourPolygonArea(sPolygon)
		if area>5000 : 
			player += 1

			meanColor = cvb.cvBlobMeanColor(blob, labelImg, img)
			#print "Mean color: r=" + str(meanColor[0]) + ", g=" + str(meanColor[1]) + ", b=" + str(meanColor[2])
			centr = cvb.cvCentroid(blob)
			print (int(centr[0]),int(centr[1]))
			dist = first_depth[int(centr[1])][int(centr[0])]
			
	
			cPolygon = cvb.cvPolygonContourConvexHull(sPolygon)
	     	
			cvb.cvRenderContourChainCode(blob.contour, imgOut)
			cvb.cvRenderContourPolygon(sPolygon, imgOut,cv.CV_RGB(0, 0, 255))
			cvb.cvRenderContourPolygon(cPolygon, imgOut,cv.CV_RGB(0, 255, 0))
	
			# Render internal contours:
			for contour in blob.internalContours: 
				cvb.cvRenderContourChainCode(contour, imgOut)
			#if comp == 10:
			print ("player =",player , "labal =" , label , "centre =",centr , "area = ",area, "dist =",dist)
			s.sendto((str(player)+ " " + str(centr[0]) + " " + str(centr[1]) +" "+ str(dist) + " ; \n"),addr)	


	#comp = comp + 1

	cv.ShowImage("test", imgOut)
	cv.ShowImage("grey", grey);
	#cv.WaitKey(0)
	#cv.DestroyWindow("test");
	return 0


cv.NamedWindow("test", 1);
cv.NamedWindow("grey", 1);
#cv.NamedWindow('Depth')
#cv.NamedWindow('Video')

cv.CreateTrackbar('threshold', 'grey', threshold,     500,  change_threshold)
cv.CreateTrackbar('depth',     'grey', current_depth, 2048, change_depth)

print('Press ESC in window to stop')

imgOut = cv.CreateImage((640,480), cv.IPL_DEPTH_8U,3)

def get_depth():
	#ghost = pretty_depth_cv(freenect.sync_get_depth()[0])
    
	return frame_convert.pretty_depth_cv(freenect.sync_get_depth()[0])


def get_video():
    return frame_convert.video_cv(freenect.sync_get_video()[0])

def init_res():
	HOST = 'localhost'    # The remote host
	HOST2 = 'localhost'
	HOST3 = 'localhost'
	PORT = 3002              # The same port as used by the server
	PORT2 = 3003
	PORT3 = 3004
	global s
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	global addr
	addr = (HOST,PORT)
	addr2 = (HOST2,PORT2)
	addr3 = (HOST3,PORT3)
	print ("socket connection : ")
	print addr , addr2
	buf = 1024


init_res()

while 1:
	comp= comp + 1
	#cv.ShowImage('Depth', get_depth())
    	#cv.ShowImage('Video', get_video())
	#cv.ShowImage("test", imgOut)
	show_blob(comp)
	if comp == 20:
		comp=0
    	if cv.WaitKey(10) == 27:
        	break

