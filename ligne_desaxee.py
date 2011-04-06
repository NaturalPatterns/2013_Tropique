#!/usr/bin/env python

from psychopy import visual, event, core#, log
import numpy as np
import Image
globalClock = core.Clock()
win = visual.Window(fullscr=True, color=[-1,-1,-1] , units='norm')
win.setRecordFrameIntervals(True)
win._refreshThreshold=1/50.0+0.004 #i've got 50Hz monitor and want to allow 4ms tolerance
downscale=0

signalTexture = -np.ones((512/2**downscale,512/2**downscale))
signalTexture[:, 512/2**downscale/2] = 1.
signal_index_array = np.arange(signalTexture.size)
stimulus = visual.PatchStim(win,tex=signalTexture,#'/Applications/PsychoPy2.app/Contents/Resources/lib/python2.6/psychopy/demos/coder/face.jpg',
#    pos=(0.0,0.0),
    size=(1900,1200), units='pix',
    opacity=1.,
    )

myMouse = event.Mouse(win=win)
myMouse.setVisible(False)
message = visual.TextStim(win, pos=(-.9,-.9), alignHoriz='left', height=.05, autoLog=False, color = (0,0,1))

X, Y = 0., 0.
offset, offset_increment = 0., 2
rotspeed, rotspeed_Increment = .1, 0.02
width, width_Increment = 2,  1

t=lastFPSupdate=0
while True:
    t=globalClock.getTime()
#    print  win.fps(), str(win.fps())
    #update fps every second
    if t-lastFPSupdate>1.0:
        lastFPSupdate=t
        message.setText(str(int(win.fps()))+  " fps / " +  str(X) + " /" +  str(Y) + " /" +  str(offset) + " " +  str(rotspeed) + " / [Esc] to quit" )
        
    for key in event.getKeys():
        if key in ['escape','q']:
            core.quit()

    X, Y = myMouse.getPos()
    wheel_dX, wheel_dY = myMouse.getWheelRel()
    rotspeed += wheel_dY*rotspeed_Increment
    offset += wheel_dX*offset_increment
    if width<0: width=1
    buttons = myMouse.getPressed()
    event.clearEvents() # get rid of other, unprocessed events

#    if np.sum(buttons)>0:
#        print buttons
#        if buttons[0]:
#            offset += offset_increment
#        elif buttons[1]:
#            offset += -offset_increment
#     
    if not(wheel_dX==0) or np.sum(buttons)>0: 
        signalTexture = -np.ones((512/2**downscale,512/2**downscale))
        middle = 512/2**downscale/2
        signalTexture[:, (offset+middle-width):(offset+middle+width-1)] = 1.
        stimulus.setTex(signalTexture.ravel()[signal_index_array].reshape(signalTexture.shape))

    stimulus.setPos((X*1200, Y*900), operation = '', units = 'norm')
    stimulus.setOri(t*rotspeed*360.0)
    stimulus.draw()
    message.draw()
    win.flip()

win.close()

