#!/usr/bin/env python

##########################################
downscale=0 # 
rotspeed, rotspeed_Increment = .001, 0.002 # en Hz?
width, width_Increment = 1,  1 # largeur de la ligne en pixels
n_line, decalage, decalage_increment = 3, 10, 1
freq, freq_Increment = .01, 0.001 # largeur de la ligne en pixels
freqx, freqx_Increment = 10.0, 0.1 # largeur de la ligne en pixels

##########################################
from psychopy import visual, event, core#, log
import numpy as np
import Image
globalClock = core.Clock()
win = visual.Window(fullscr=True, color=[-1,-1,-1] , units='norm')
win.setRecordFrameIntervals(True)
win._refreshThreshold=1/20.0+0.004 #i've got 50Hz monitor and want to allow 4ms tolerance

# TODO : def texture():
signalTexture = -np.ones((512/2**downscale,512/2**downscale))

size_line = signalTexture.shape[0]
signal_index_array = np.arange(signalTexture.size)
stimulus = visual.PatchStim(win,tex=signalTexture,#'/Applications/PsychoPy2.app/Contents/Resources/lib/python2.6/psychopy/demos/coder/face.jpg',
#    pos=(0.0,0.0),
    size=(1900,1200), units='pix',
    opacity=1.,
    )

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
            message.setText(str(int(win.fps()))+  " fps / " +  str(freqx) + " /" +  str(freq) + " / " +  str(rotspeed) + " / [Esc] to quit" )
        else:
            message.setText('' )
        
    for key in event.getKeys():
        if key in ['s']:
            showText = not(showText)
        elif key in ['d']:
            decalage += decalage_increment
        elif key in ['f']:
            decalage += -decalage_increment
        elif key in ['escape','q']:
            core.quit()

    X, Y = myMouse.getPos()
    wheel_dX, wheel_dY = myMouse.getWheelRel()
    freq += wheel_dY*freq_Increment
    freqx += wheel_dX*freqx_Increment
    if width==0: width=1
    event.clearEvents() # get rid of other, unprocessed events

    # if not(wheel_dX==0): # or (key in ['d']) or (key in ['f']): 
    signalTexture = -np.ones((512/2**downscale,512/2**downscale))
    middle = 512/2**downscale/2
    for i_line in range(n_line):
        pulse = np.sin( 2*np.pi * (freqx * np.linspace(0, 1 , size_line) + t*freq*360.0))
        signalTexture[:, (middle + i_line*decalage)] = pulse
        # TODO : wtf?
    stimulus.setTex(signalTexture.ravel()[signal_index_array].reshape(signalTexture.shape))

    stimulus.setPos((X*1200, Y*900), operation = '', units = 'norm')
    stimulus.setOri(t*rotspeed*360.0)
    stimulus.draw()
    message.draw()
    win.flip()

win.close()

