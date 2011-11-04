#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Une série de 3 lignes parallèles qui tournent. le centre de rotation est desaxé par rapport à la ligne.

    interaction souris:
        position souris: centre du stimulus
        scroll up/down: change la vitesse de rotation
        scroll left/right: change  le desaxage
    touches d'interaction:
        s: showText
        x: augmente longueur des lignes
        c: diminue longueur des lignes
        d: augmente écart entre les lignes
        f: diminue écart entre les lignes
       escape ou q: quitte
         
"""
##########################################
downscale= 0 # 
rotspeed, rotspeed_Increment = .001, 0.002 # en Hz?
width, width_Increment =1,  1 # largeur de la ligne en pixels
n_line, decalage, decalage_increment = 3, 10, 1
size_h, size_h_increment = 1., .02
X, Y = 0., 0.
offset, offset_increment = 0., 2
##########################################

from psychopy import visual, event, core#, log
import numpy as np
import Image
globalClock = core.Clock()
win = visual.Window(fullscr=True, color=[-1,-1,-1] , units='norm')
win.setRecordFrameIntervals(True)
win._refreshThreshold=1/50.0+0.004 #i've got 50Hz monitor and want to allow 4ms tolerance
downscale=0

signalTexture = -np.ones((512/2**downscale,512/2**downscale))
stimulus = visual.PatchStim(win,tex=signalTexture,
    size=(size_h, size_h), units='height',
    opacity=1.,
    )
signal_index_array = np.arange(signalTexture.size)

def texture(offset, width, decalage, n_line):
    signalTexture = -np.ones((512/2**downscale,512/2**downscale))
    middle = 512/2**downscale/2
    for i_line in range(n_line):
        signalTexture[:, (offset+middle-width + i_line*decalage):(offset+middle+width-1 + i_line*decalage)] = 1.
    return signalTexture

signalTexture = texture(offset, width, decalage, n_line)
stimulus.setTex(signalTexture.ravel()[signal_index_array].reshape(signalTexture.shape))


myMouse = event.Mouse(win=win)
myMouse.setVisible(False)
message = visual.TextStim(win, pos=(-.9,-.9), alignHoriz='left', height=.05, autoLog=False, color = (0,0,1))

showText = True
t=lastFPSupdate=0
while True:
    t=globalClock.getTime()
#    print  win.fps(), str(win.fps())
    #update fps every second
    if t-lastFPSupdate>1.0:
        lastFPSupdate=t
        if showText:
            message.setText(str(int(win.fps()))+  " fps / " +  str(X) + " /" +  str(Y) + " /" +  str(offset) + " " +  str(rotspeed) + " / [Esc] to quit" )
        else:
            message.setText('' )
     
    for key in event.getKeys():
        if key in ['escape','q']:
            core.quit()
        elif key in ['s']:
            showText = not(showText)
        elif key in ['x']:
            size_h += size_h_increment
            stimulus.setSize((size_h, size_h))
        elif key in ['c']:
            size_h += -size_h_increment
            stimulus.setSize((size_h, size_h))

    X, Y = myMouse.getPos()
    wheel_dX, wheel_dY = myMouse.getWheelRel()
    rotspeed += wheel_dY*rotspeed_Increment
    offset += wheel_dX*offset_increment
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
        signalTexture = texture(offset, width, decalage, n_line)
        stimulus.setTex(signalTexture.ravel()[signal_index_array].reshape(signalTexture.shape))

    stimulus.setPos((X, Y), operation = '')
    stimulus.setOri(t*rotspeed*360.0)
    stimulus.draw()
    message.draw()
    win.flip()

win.close()

