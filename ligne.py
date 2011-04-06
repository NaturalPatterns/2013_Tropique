#!/usr/bin/env python

##########################################
downscale= 0 # 
rotspeed, rotspeed_Increment = .001, 0.002 # en Hz?
width, width_Increment =1,  1 # largeur de la ligne en pixels
n_line, decalage, decalage_increment = 3, 10, 1
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

def texture(width, decalage, n_line):
    signalTexture = -np.ones((512/2**downscale,512/2**downscale))
    middle = 512/2**downscale/2
    for i_line in range(n_line):
        signalTexture[:, (middle-width + i_line*decalage):(middle+width-1 + i_line*decalage)] = 1.
    return signalTexture

signalTexture = texture(width, decalage, n_line)
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
            message.setText(str(int(win.fps()))+  " fps / " +  str(decalage) + " /" +  str(Y) + " /" +  str(width) + " " +  str(rotspeed) + " / [Esc] to quit" )
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
            signalTexture = texture(width, decalage, n_line)
            stimulus.setTex(signalTexture.ravel()[signal_index_array].reshape(signalTexture.shape))
        elif key in ['f']:
            decalage += -decalage_increment
            signalTexture = texture(width, decalage, n_line)
            stimulus.setTex(signalTexture.ravel()[signal_index_array].reshape(signalTexture.shape))
        elif key in ['escape','q']:
            core.quit()

    X, Y = myMouse.getPos()
    wheel_dX, wheel_dY = myMouse.getWheelRel()
    rotspeed += wheel_dY*rotspeed_Increment
    width += wheel_dX*width_Increment
    if width==0: width=1
    event.clearEvents() # get rid of other, unprocessed events

    if not(wheel_dX==0): # or (key in ['d']) or (key in ['f']): 
            signalTexture = texture(width, decalage, n_line)
            stimulus.setTex(signalTexture.ravel()[signal_index_array].reshape(signalTexture.shape))

    print width, decalage, n_line, signalTexture.mean()
    stimulus.setPos((X, Y), operation = '')
    stimulus.setOri(t*rotspeed*360.0)
    stimulus.draw()
    message.draw()
    win.flip()

win.close()

