#!/usr/bin/env python
import freenect
import cv
import frame_convert

cv.NamedWindow('Depth')
cv.NamedWindow('Video')
print('Press ESC in window to stop')

cv.NamedWindow('first')
cv.NamedWindow('diff')
cv.NamedWindow('sec')

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

def get_depth():
    return frame_convert.pretty_depth_cv(freenect.sync_get_depth()[0])


def get_video():
    return frame_convert.video_cv(freenect.sync_get_video()[0])

def threshold_image(n=[]):
	image  = (freenect.sync_get_depth()[0])
	if len(n) < 5:
		n.append(cv.CloneMat(image))
		return image
	else :
		original = n[4]
		differenceImage = cv.CloneMat(image)
		blackimage = cv.CloneMat(image)
		cv.AbsDiff(image, original, differenceImage)
		#print type(image)
		print cv.GetSize (differenceImage)

		gray = cv.CreateImage ( cv.GetSize (differenceImage) , 8 , 1 )
		img_cv = array2cv(image)
		print cv.GetSize (gray)
		#gray = cv.CreateImage ( cv.GetSize (img_cv) , 8 , 1 )
		#cv.Invert(img_cv,img_cv,cv.CV_LU) 
		thresholdValue = 200
		#rel_ima =frame_convert.pretty_depth_cv (differenceImage)
		cv.Threshold(gray , gray , thresholdValue , 255 , cv.CV_THRESH_BINARY)
	        #cv.Smooth ( differenceImage , differenceImage , cv.CV_MEDIAN , 15)
		#cv.Smooth ( image , image , cv.CV_MEDIAN , 15)
		result  = cv.CloneMat(image)
		cv.SetZero(result)
		#cv.And(image,image,result, gray)
		cv.ShowImage('sec', gray)
		return gray



cv.ShowImage('first',frame_convert.pretty_depth_cv(freenect.sync_get_depth()[0]) )
img_first = frame_convert.pretty_depth_cv(freenect.sync_get_depth()[0])


while 1:
    cv.ShowImage('diff', threshold_image())
    cv.ShowImage('Depth', get_depth())
    cv.ShowImage('Video', get_video())
    if cv.WaitKey(10) == 27:
        break
