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



threshold = 250
current_depth = 720
global num_detect
num_detect = 0

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
global threshold
global current_depth

def show_blob():
	depth, timestamp = freenect.sync_get_depth()
	depth = 255 * np.logical_and(depth >= current_depth - threshold,
                                 depth <= current_depth + threshold)
	depth = depth.astype(np.uint8)
    
	#print depth
	font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8) #Creates a font

	image = cv.CreateImageHeader((depth.shape[1], depth.shape[0]),cv.IPL_DEPTH_8U,1)

	cv.SetData(image, depth.tostring(),depth.dtype.itemsize * depth.shape[1])
	cv.PutText(image,"Hello World", (5,20),font, 255) #Draw the text
	grey = image
	
	img = frame_convert.video_cv(freenect.sync_get_video()[0])

	#print type (img)

	IPL_DEPTH_LABEL = 32
	labelImg = cv.CreateImage(cv.GetSize(grey), IPL_DEPTH_LABEL, 1)

	blobs = cvb.CvBlobs()
	result = cvb.cvLabel(grey,labelImg,blobs)

	#imgOut = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U,3)
	cv.Zero(imgOut);
	#cvb.cvRenderBlobs(labelImg, blobs, img, imgOut);
	num_detect = 0
	# Render contours:
	print ("new frame")
	for label, blob in blobs.iteritems(): 
		polygon = cvb.cvConvertChainCodesToPolygon(blob.contour)
		sPolygon = cvb.cvSimplifyPolygon(polygon, 10.)
		area = cvb.cvContourPolygonArea(sPolygon)
		if area>5000 : 
			num_detect = num_detect + 1
			print label
			meanColor = cvb.cvBlobMeanColor(blob, labelImg, img)
			print "Mean color: r=" + str(meanColor[0]) + ", g=" + str(meanColor[1]) + ", b=" + str(meanColor[2])
			centr = cvb.cvCentroid(blob)
			print ("centre =",centr)
			print ("area = ",area)
	
			cPolygon = cvb.cvPolygonContourConvexHull(sPolygon)
	     	
			cvb.cvRenderContourChainCode(blob.contour, imgOut)
			cvb.cvRenderContourPolygon(sPolygon, imgOut,cv.CV_RGB(0, 0, 255))
			cvb.cvRenderContourPolygon(cPolygon, imgOut,cv.CV_RGB(0, 255, 0))
	
			# Render internal contours:
			for contour in blob.internalContours: 
				cvb.cvRenderContourChainCode(contour, imgOut)
	

	print ("nombre_joueurs = ", num_detect)

	cv.ShowImage("test", imgOut)
	cv.ShowImage("grey", grey);
	#cv.WaitKey(0)
	#cv.DestroyWindow("test");
	return 0


cv.NamedWindow("test", 1);
#cv.NamedWindow('Depth')
#cv.NamedWindow('Video')
print('Press ESC in window to stop')

imgOut = cv.CreateImage((640,480), cv.IPL_DEPTH_8U,3)

def get_depth():
	#ghost = pretty_depth_cv(freenect.sync_get_depth()[0])
    
	return frame_convert.pretty_depth_cv(freenect.sync_get_depth()[0])


def get_video():
    return frame_convert.video_cv(freenect.sync_get_video()[0])


while 1:
    	#cv.ShowImage('Depth', get_depth())
    	#cv.ShowImage('Video', get_video())
	#cv.ShowImage("test", imgOut)
	show_blob()
    	if cv.WaitKey(10) == 27:
        	break

