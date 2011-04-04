#!/usr/bin/env python

# rapidly swipe an image on the screen, unseen in normal viewing conditions except when doing a proper saccade

from psychopy import visual, event, core, log
import numpy as np
import Image
globalClock = core.Clock()
win = visual.Window([1900,1200], fullscr=True, units='pix')
win.setRecordFrameIntervals(True)
win._refreshThreshold=1/50.0+0.004 #i've got 50Hz monitor and want to allow 4ms tolerance
#set the log module to report warnings to the std output window (default is errors only)
log.console.setLevel(log.WARNING)

#fixSpot = visual.PatchStim(win,tex="none", mask="gauss",
#        pos=(0,0), size=(50,50),color='red', autoLog=False)
#
#import scipy
# noiseTexture = np.array(Image.open('/Applications/PsychoPy2.app/Contents/Resources/lib/python2.6/psychopy/demos/coder/face.jpg'))
# noiseTexture /= np.max(np.abs(noiseTexture))*2 -1
downscale=2
#noiseTexture = scipy.random.rand(512/2**downscale,512/2**downscale)*2.0-1
#index_array = np.arange(noiseTexture.size)
#noise = visual.PatchStim(win, tex=noiseTexture, 
#    pos=(0.0,0), size=(1900,1200), units='pix',
#    opacity=1.,
#    interpolate=False)

#filename = '/Volumes/tera/10-12-31_RTC/10-03-23_cnprs/spip/prive/vignettes/deb.png'
#signalTexture = scipy.random.rand(64/2**downscale,64/2**downscale)*2.0-1
signalTexture = np.zeros((512/2**downscale,512/2**downscale))
signalTexture[:, 512/2**downscale/2] = 1.
signal_index_array = np.arange(signalTexture.size)
stimulus = visual.PatchStim(win,tex=signalTexture,#'/Applications/PsychoPy2.app/Contents/Resources/lib/python2.6/psychopy/demos/coder/face.jpg',
#    pos=(0.0,0.0),
    size=(1900,1200), units='pix',
    opacity=1.,
    )

#stimulus = visual.SimpleImageStim(win,image='/Applications/PsychoPy2.app/Contents/Resources/lib/python2.6/psychopy/demos/coder/face.jpg',
#    pos=(0.0,0.0), units ='norm', contrast =.3
#    )

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
b.settimeout(5)


t=lastFPSupdate=lastT=0
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

    wheel_dX, wheel_dY = myMouse.getWheelRel()
    position += wheel_dY*position_Increment
    event.clearEvents()#get rid of other, unprocessed events
    
#    if True:#t-lastT>.05:
#        lastT=t
#        np.random.shuffle(index_array)
#    
#    noise.setTex(noiseTexture.ravel()[index_array].reshape(noiseTexture.shape))
#    noise.draw()

    try :
        dat = b.recvfrom(1024)
        position = float(dat[0])
        print position
    except:
        print ("nodata")
#	else :
#		print float(dat[0])


    x =  position / 3.5 *2 -1 #t*speed%2 -1 # relative coordinate between -1 and 1
    x = np.int( (x+1)/2 *128 )/128. *2 - 1 # taking the integer part according to the texture's scale
    x = x*1900/2 # scaling to pix units
#
#    if abs(abs(x)-1900/2)<300: 
#        np.random.shuffle(signal_index_array)
#        stimulus.setTex(signalTexture.ravel()[signal_index_array].reshape(signalTexture.shape))

    stimulus.setPos((x, 0))#32*1200 / 128))
    stimulus.draw()
#    
#    if abs(abs(x)-400)<20: 
#        fixSpot.setPos((np.sign(x)*800, -400.))
#        fixSpot.draw()
#        
#    fixSpot.setPos((x,-400))
#    fixSpot.draw()
        
        
    message.draw()

    win.flip()
import pylab
pylab.plot(win.frameIntervals)
pylab.show()
win.saveFrameIntervals(fileName=None, clear=True)

win.close()

