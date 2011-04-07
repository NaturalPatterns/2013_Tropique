#!/usr/bin/env python
##########################################
downscale=0 # 
rotspeed, rotspeed_Increment = .001, 0.002 # en Hz?
n_line = 36
size_h, size_h_increment = 1., .02
radius, radius_increment  = .4, .02
width, width_increment = .01,  .001 # largeur de la ligne en pixels
length, length_increment  = .5, .01
##########################################
from psychopy import visual, event, core#, log
import numpy as np
import Image
globalClock = core.Clock()
win = visual.Window(fullscr=True, color=[-1,-1,-1] , units='norm')
win.setRecordFrameIntervals(True)
win._refreshThreshold=1/20.0+0.004 #i've got 50Hz monitor and want to allow 4ms tolerance
X, Y = 0., 0.
phase = np.linspace(0,2*np.pi, n_line, endpoint=False)
def update_caroussel(X, Y, n_line, angle = 0.):
    global phase
#    XY = np.zeros((2,0))
#    radius_ = np.logspace(-1,0, N, endpoint=False) * radius
#    for i_line in range(n_line):
    phase += 0.001* np.random.randn(n_line)
    XY = np.array([X + radius*np.cos(phase + angle), Y + radius*np.sin(phase + angle)])
#    XY = np.hstack((XYs, XY))
    return XY.T, phase

def caroussel(n_line, width, length, angle = 0.):
    XY, phase = update_caroussel(X, Y, n_line, angle)
    global_lines = visual.ElementArrayStim(win, nElements=XY.shape[0], sizes=(length, width), elementTex='sqr', # sfs=3,
                                                    rgbs= np.array([1,1,1]), xys = XY, oris = phase  * 360 / 2. / np.pi  , units='height')
    return global_lines

global_lines = caroussel(n_line, width, length, angle = 0.)


showText = True
myMouse = event.Mouse(win=win)
myMouse.setVisible(False)
message = visual.TextStim(win, pos=(-.9,-.9), alignHoriz='left', height=.05, autoLog=False, color = (0,0,1))


t=lastFPSupdate=0
while True:
    t=globalClock.getTime()
#    print  win.fps(), str(win.fps())
    #update fps every second
    if t-lastFPSupdate>1.0:
        lastFPSupdate=t
        if showText:
            message.setText(str(int(win.fps()))+  " fps / " +  str(width) + " /" +  str(length) + " / " +  str(rotspeed) + " / s - d - f - w -x - c - v" )
        else:
            message.setText('' )
        
    for key in event.getKeys():
        if key in ['s']:
            showText = not(showText)
        elif key in ['d']:
            width += -width_increment
            global_lines = caroussel(n_line, width, length, angle = 0.)
        elif key in ['f']:
            width += width_increment
            global_lines = caroussel(n_line, width, length, angle = 0.)
        elif key in ['w']:
            length += -length_increment
            global_lines = caroussel(n_line, width, length, angle = 0.)
        elif key in ['x']:
            length += length_increment
            global_lines = caroussel(n_line, width, length, angle = 0.)
        elif key in ['-','[','c']:
            n_line -=1
            if n_line==0: n_line=1
            global_lines = caroussel(n_line, width, length, angle = 0.)
        elif key in ['+',']','v']:
            n_line+=1
            global_lines = caroussel(n_line, width, length, angle = 0.)
        elif key in ['escape','q']:
            core.quit()

    X, Y = myMouse.getPos()
    wheel_dX, wheel_dY = myMouse.getWheelRel()
    rotspeed += wheel_dY*rotspeed_Increment
    radius += wheel_dX*radius_increment 
    event.clearEvents() # get rid of other, unprocessed events

    angle = t*rotspeed *2*np.pi
    newXY, phase = update_caroussel(X, Y, n_line, angle)
#    print phased
    global_lines.setXYs( newXY )
    global_lines.setOris( (phase + angle) * 360 / 2. / np.pi)
    global_lines.draw()
    
    message.draw()
    win.flip()

win.close()

