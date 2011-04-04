#!/usr/bin/env python

from psychopy import visual, event, core#, log
import numpy as np
import Image
globalClock = core.Clock()
win = visual.Window([1900,1200], fullscr=True, units='pix')
#win.setRecordFrameIntervals(True)
#win._refreshThreshold=1/50.0+0.004 #i've got 50Hz monitor and want to allow 4ms tolerance
#set the log module to report warnings to the std output window (default is errors only)
log.console.setLevel(log.WARNING)


downscale=2

signalTexture = np.zeros((512/2**downscale,512/2**downscale))
signalTexture[:, 512/2**downscale/2] = 1.
signal_index_array = np.arange(signalTexture.size)
stimulus = visual.PatchStim(win,tex=signalTexture,#'/Applications/PsychoPy2.app/Contents/Resources/lib/python2.6/psychopy/demos/coder/face.jpg',
#    pos=(0.0,0.0),
    size=(1900,1200), units='pix',
    opacity=1.,
    )

myMouse = event.Mouse(win=win)
message = visual.TextStim(win, pos=(-900,-450), alignHoriz='left', height=40, autoLog=False, color = (0,0,1))

position, position_Increment = 2.1, 0.02

import socket

#description res
host = '192.168.1.4'
port = 3002
buf = 1024

b= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
addr =(host,port)
print addr
b.bind(addr)
b.settimeout(0)


t=lastFPSupdate=0
while True:
    t=globalClock.getTime()
#    print  win.fps(), str(win.fps())
    #update fps every second
    if t-lastFPSupdate>1.0:
        lastFPSupdate=t
        message.setText(str(int(win.fps()))+  " fps / " +  str(position) + " / [Esc] to quit" )
    for key in event.getKeys():
        if key in ['escape','q']:
            core.quit()

    try :
        dat = b.recvfrom(1024)
        position = float(dat[0])
        print position
        message.setText(str(int(win.fps()))+  " fps / " +  str(position) + " / [Esc] to quit" )
    except:
        pass
#        print ("nodata")
    else:
        print float(dat[0])

    x =  position / 3.5 *2 -1 #t*speed%2 -1 # relative coordinate between -1 and 1
    x = np.int( (x+1)/2 *128 )/128. *2 - 1 # taking the integer part according to the texture's scale
    x = x*1900/2 # scaling to pix units

    stimulus.setPos((x, 0))#32*1200 / 128))
    stimulus.draw()

    message.draw()

    win.flip()

win.close()

