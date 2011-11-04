#!/usr/bin/env python
##########################################
downscale=0 # 
rotspeed, rotspeed_Increment = .001, 0.002 # en Hz?
width, width_Increment = 1,  1 # largeur de la ligne en pixels
n_line, decalage, decalage_increment = 3, 10, 1
freq, freq_Increment = .01, 0.001 # largeur de la ligne en pixels
freqx, freqx_Increment = 10.0, 0.1 # largeur de la ligne en pixels
size_h, size_h_increment = 1., .02
##########################################
from psychopy import visual, event, core#, log
import numpy as np
import Image
globalClock = core.Clock()
win = visual.Window(fullscr=True, color=[-1,-1,-1] , units='norm')
win.setRecordFrameIntervals(True)
win._refreshThreshold=1/20.0+0.004 #i've got 50Hz monitor and want to allow 4ms tolerance

signalTexture = -np.ones((512/2**downscale,512/2**downscale))
stimulus = visual.PatchStim(win,tex=signalTexture,
    size=(size_h, size_h), units='height',
    opacity=1.,
    )
signal_index_array = np.arange(signalTexture.size)
size_line = signalTexture.shape[0]

def texture(freqx, freq, width, decalage, n_line, t):
    signalTexture = -np.ones((512/2**downscale,512/2**downscale))
    middle = 512/2**downscale/2
    pulse = np.sin( 2*np.pi * (freqx * np.linspace(0, 1 , size_line) + t*freq*360.0))
    for i_line in range(n_line):
        signalTexture[:, middle-width + i_line*decalage] = pulse
    return signalTexture

signalTexture = texture(freqx, freq, width, decalage, n_line, 0.)
stimulus.setTex(signalTexture.ravel()[signal_index_array].reshape(signalTexture.shape))


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
        elif key in ['x']:
            size_h += size_h_increment
            stimulus.setSize((size_h, size_h))
        elif key in ['c']:
            size_h += -size_h_increment
            stimulus.setSize((size_h, size_h))
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

    signalTexture = texture(freqx, freq, width, decalage, n_line, t)
    stimulus.setTex(signalTexture.ravel()[signal_index_array].reshape(signalTexture.shape))

    stimulus.setPos((X, Y), operation = '')
    stimulus.setOri(t*rotspeed*360.0)
    stimulus.draw()
    message.draw()
    win.flip()

win.close()

