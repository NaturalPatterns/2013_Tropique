#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
    Couloir de lignes paralleles dont le centre change avec la position de la kinect
    
"""
fullscreen = True #False # 
import socket
import signal, sys
#print socket.__version__
#description res
host = '' # '127.0.0.1'#192.168.1.4'
port = 50042
buf = 1024 # 4096
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# socket.SOCK_DGRAM) # 
#addr =(host,port)
#print addr
#s.bind(addr)
#s.setblocking(0)
#s.settimeout(0)
#s.settimeout(5)
s.setblocking(1)
s.connect((host, port))
##########################################
from psychopy import visual, event, core#, log
import numpy as np
#import Image
globalClock = core.Clock()
win = visual.Window(fullscr=fullscreen, color=[-1,-1,-1] , units='norm')
win.setRecordFrameIntervals(True)
win._refreshThreshold=1/20.0+0.004 #i've got 50Hz monitor and want to allow 4ms tolerance
X, Y = 0., 0.
n_line = 36
phase = np.linspace(0,2*np.pi, n_line, endpoint=False)
def update_caroussel(X, Y, n_line, radius, angle):
    global phase
#    XY = np.zeros((2,0))
#    radius_ = np.logspace(-1,0, N, endpoint=False) * radius
#    for i_line in range(n_line):
    XY = np.array([X + radius*np.sign(np.cos(phase)), Y + radius*np.tan(phase)])
#    phase = np.linspace(0,2*np.pi, n_line, endpoint=False) + angle
#    XY = np.array([X + radius*np.cos(phase), Y + radius*np.sin(phase)])
#    XY = np.hstack((XYs, XY))
    return XY.T, phase

def caroussel(n_line, width, length, radius, angle):
    global phase
    XY, phase = update_caroussel(X, Y, n_line, radius, angle)
    global_lines = visual.ElementArrayStim(win, nElements=XY.shape[0], sizes=(width, length), elementTex='sqr', # sfs=3,
                                                    rgbs= np.array([1,1,1]), xys = XY, oris = 0.  , units='height') #  phase  * 360 / 2. / np.pi
    return global_lines

#################################################
def handler(signum, frame):
    s.close()
    win.close()
    sys.exit()

def main():
    global phase
    ##########################################
    rotspeed, rotspeed_Increment = .001, 0.002 # en Hz?
    width, width_increment = .5,  .01 # largeur de la ligne en pixels
    n_line = 36
#    size_h, size_h_increment = 1., .02
    radius, radius_increment  = .35, .02
    length, length_increment  = .005, .001
    dX, dY = 0. , 0.
    az_m, az_r, el_m,  el_r = 0., -1.1, 0., 1.

    ##########################################
    print('Press Ctrl-C in terminal to stop')
    signal.signal(signal.SIGINT, handler)
    global_lines = caroussel(n_line, width, length, radius, 0.)
    showText = True
    myMouse = event.Mouse(win=win)
    myMouse.setVisible(False)
    message = visual.TextStim(win, pos=(-.9,-.9), alignHoriz='left', height=.04, autoLog=False, color = (0,0,1))
    t=lastFPSupdate=0
    confused = 1.
    walk = np.zeros((n_line, 3))

    while True:
        t=globalClock.getTime()

        # asking the kinect to send the data
#   TODO : envoyer un status (ready, quitting...)
        s.send('ready')
#        print ('before', t)
        # retrieve the data
        try :
#            dat = s.recvfrom(buf)
            dat  = s.recv(buf)
        except:
            print ("nodata")
        else :
#            dat_brut=str(dat[0])
            
            datasplit1 = dat.split(",")
            prof_m =  float(datasplit1[0])
            datasplit2 = datasplit1[1].split(",")
            az_m =  float (datasplit2[0])
            el_m = float(datasplit1[2])
            print (t, "receiv = ", prof_m, az_m , el_m)
            dX_ , dY_ = prof_m, el_m
            if dX_ >   .99*4.5: 
#                print('confused!')
                confused = (1. - 0.01) * (confused) +  0.01 *1
                #noData=True
            else:
                #noData = False
                #print dX_
                confused = (1. - 0.01) * (confused)
                dX, dY = (1- 1./10) * dX + 1./10 * (dX_ - 4.5/2.)/ az_r, (1- 1./10) * dY + 1./10 * dY_ / el_r

#        print ('after', t)

    #    print  win.fps(), str(win.fps())
        #update fps every second
        if t-lastFPSupdate>1.0:
            lastFPSupdate=t
            if showText:
                message.setText(str(int(win.fps()))+  " fps / " +  str(width) + " /" +  str(length) + " / " +  str(rotspeed) + " / " +  str(confused) + " / s - d - f - w -x - c - v" )
            else:
                message.setText('' )
            
        for key in event.getKeys():
            if key in ['s']:
                showText = not(showText)
            elif key in ['d']:
                width += -width_increment
                global_lines = caroussel(n_line, width, length, radius, angle = 0.)
            elif key in ['f']:
                width += width_increment
                global_lines = caroussel(n_line, width, length, radius, angle = 0.)
            elif key in ['w', 'a']:
                length += - length_increment
                global_lines = caroussel(n_line, width, length, radius, angle = 0.)
            elif key in ['x']:
                length += length_increment
                global_lines = caroussel(n_line, width, length, radius, angle = 0.)
            elif key in ['-','[','c']:
                n_line -=1
                if n_line==0: n_line=1
                global_lines = caroussel(n_line, width, length, radius, angle = 0.)
            elif key in ['+',']','v']:
                n_line+=1
                global_lines = caroussel(n_line, width, length, radius, angle = 0.)
            elif key in ['escape','q']:
                core.quit()

        X, Y = myMouse.getPos()
        wheel_dX, wheel_dY = myMouse.getWheelRel()
        rotspeed += wheel_dY*rotspeed_Increment
        radius += wheel_dX*radius_increment 
        event.clearEvents() # get rid of other, unprocessed events

        angle = t*rotspeed*2*np.pi
        newXY, phase = update_caroussel(2.*X + dX, 2.*Y+dY, n_line, radius, angle)

        walk += 0.001* np.random.randn(n_line,3)
        walk *= 1 + confused - .5
        
        global_lines.setXYs( newXY + walk[:,0:2] )
#        global_lines.setOris( (phase +  angle + .0 * walk[:,2] ) * 360 / 2. / np.pi)
        global_lines.draw()
        

        message.draw()
        win.flip()

    s.send('done')
    s.close()
    win.close()

if __name__ == "__main__":
    main()


