#!/usr/bin/env python
#
# matplotlib now has a PolarAxes class and a polar function in the
# matplotlib interface.  This is considered alpha and the interface
# may change as we work out how polar axes should best be integrated
#
# The only function that has been tested on polar axes is "plot" (the
# pylab interface function "polar" calls ax.plot where ax is a
# PolarAxes) -- other axes plotting functions may work on PolarAxes
# but haven't been tested and may need tweaking.
#
# you can get get a PolarSubplot instance by doing, for example
#
#   subplot(211, polar=True)
#
# or a PolarAxes instance by doing
#   axes([left, bottom, width, height], polar=True)
#
# The view limits (eg xlim and ylim) apply to the lower left and upper
# right of the rectangular box that surrounds to polar axes.  Eg if
# you have
#
#  r = arange(0,1,0.01)
#  theta = 2*pi*r
#
# the lower left corner is 5/4pi, sqrt(2) and the
# upper right corner is 1/4pi, sqrt(2)
#
# you could change the radial bounding box (zoom out) by setting the
# ylim (radial coordinate is the second argument to the plot command,
# as in MATLAB, though this is not advised currently because it is not
# clear to me how the axes should behave in the change of view limits.
# Please advise me if you have opinions.  Likewise, the pan/zoom
# controls probably do not do what you think they do and are better
# left alone on polar axes.  Perhaps I will disable them for polar
# axes unless we come up with a meaningful, useful and functional
# implementation for them.
#
# See the pylab rgrids and thetagrids functions for
# information on how to customize the grid locations and labels
import matplotlib
import numpy as np
import time



####
matplotlib.use('GTKAgg') # do this before importing pylab

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show, rc, grid

import socket
import signal, sys
#print socket.__version__
#description res
host = 'localhost' # '127.0.0.1'#192.168.1.4'
port = 3002
buf = 1024 # 4096

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)# socket.SOCK_DGRAM) # 
#addr =(host,port)
#print addr
#s.bind(addr)
#s.setblocking(0)
#s.settimeout(0)
#s.settimeout(5)
s.setblocking(1)
s.connect((host, port))

fig = plt.figure()



def animate():
    n = 0
    tstart = time.time()                 # for profiling
    '''x = np.arange(0, 2*np.pi, 0.01)        # x-array
    line, = ax.plot(x, np.sin(x))
    '''
    for i in np.arange(1,2000):
        #line.set_ydata(np.sin(x+i/10.0))  # update the data
	#s.send('ready')
#        print ('before', t)
        # retrieve the data
        '''try :
#            dat = s.recvfrom(buf)
		dat  = s.recv(buf)
        except:
		print ("nodata")
        else :
#            dat_brut=str(dat[0])
		print dat 
	'''
	n = n+0.01
	r = n
	theta= 0
	#s.flush()
	ax.plot(theta, r,'d', markersize=8, markerfacecolor='blue')
	ax.set_rmax(2.0)
	#grid(True)
	print n
	fig.canvas.draw()                         # redraw the canvas
    print 'FPS:' , 200/(time.time()-tstart)
    raise SystemExit



# radar green, solid grid lines
rc('grid', color='#316931', linewidth=1, linestyle='-')
rc('xtick', labelsize=15)
rc('ytick', labelsize=15)

# force square figure and square axes looks better for polar, IMO
width, height = matplotlib.rcParams['figure.figsize']
size = min(width, height)
# make a square figure
#fig = figure(figsize=(size, size))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True, axisbg='#d5de9c')

#r = np.arange(0, 3.0, 0.01)
#theta = 2*np.pi*r
#print r


import gobject
print 'adding idle'
gobject.idle_add(animate)
print 'showing'
plt.show()


'''
while 1:

	r = 1
	theta= 0
	
	ax.plot(theta, r,'d', markersize=8, markerfacecolor='blue')
	ax.set_rmax(2.0)
	grid(True)
	print 'hello'
	ax.set_title("And there was much rejoicing!", fontsize=20)
	show()
	print 'max'

'''

