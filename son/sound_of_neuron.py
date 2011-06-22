# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:34:49 2011

@author: -
"""

try:
    import pyaudio
    AUDIO = True
except:
    print('Could not import pyaudio, disabling sound')
    AUDIO = False

#import numpy as np
#
#spike = 255*np.ones(45) # that's a crude spike!
#
#
#if AUDIO:
#    # open audio stream to the speakers
#    p = pyaudio.PyAudio()
#    # initialize loudspeaker
#    stream = p.open(format=pyaudio.paInt16,
#                channels=1,
#                rate=44100,
#                output=True)

import numpy as np
#import time

PLOT = False
###### Set up the standard CUBA example ######
from brian import *
from brian.library.ionic_currents import *
from brian.library.random_processes import *

simulation_clock=Clock(dt=0.1*ms)
record_clock=Clock(dt=0.0227272*ms)

# Parameters
C = 281 * pF
gL = 30 * nS
taum = C / gL
EL = -70.6 * mV
VT = -50.4 * mV
DeltaT = 2 * mV
Vcut = VT + 5 * DeltaT

# Pick an electrophysiological behaviour
tauw, a, b, Vr = 144 * ms, 4 * nS, 0.0805 * nA, -70.6 * mV # Regular spiking (as in the paper)
#tauw,a,b,Vr=20*ms,4*nS,0.5*nA,VT+5*mV # Bursting
#tauw,a,b,Vr=144*ms,2*C/(144*ms),0*nA,-70.6*mV # Fast spiking

eqs = """
dvm/dt=(gL*(EL-vm)+gL*DeltaT*exp((vm-VT)/DeltaT)+I-w)/C : volt
dw/dt=(a*(vm-EL)-w)/tauw : amp
I : amp
"""

neuron = NeuronGroup(1, model=eqs, threshold=Vcut, reset="vm=Vr;w+=b", freeze=True, clock=simulation_clock)
neuron.vm = EL
trace = StateMonitor(neuron, 'vm', record=0, clock=record_clock)

for i in range(1000):
    neuron.I = np.random.rand() * nA
    run(10 * ms)   

plot(trace.times / ms, trace[0] / mV)
show()


import pyaudio
import wave
import sys

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = chunk)


wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(trace[0])
wf.close()

####### Real time plotting stuff ######
#
#if PLOT:
#    #The ion() command switches pylab's "interactive mode" on
#    ion()
#    # We set up the plot with the correct axes
#    subplot(211)
#    # Note that we have to store a copy of the objects (plot lines) whose data
#    # we will update in real time
#    rasterline, = plot([], [], '.') # plot points, hence the '.'
#    axis([0, 1, 0, N])
#    subplot(212)
#    traceline, = plot([], []) # plot lines, hence no '.'
#    axis([0, 1, -0.06, -0.05])
#    
#
## This network operation updates the graphics every 10ms of simulated time
#@network_operation(clock=EventClock(dt=10*ms))
#def draw_gfx():
#    # This returns two lists i, t of the neuron indices and spike times for
#    # all the recorded spikes so far
#    if PLOT:
#        i, t = zip(*M.spikes)
#        # Now we update the raster and trace plots with this new data
#        rasterline.set_xdata(t)
#        rasterline.set_ydata(i)
#        traceline.set_xdata(trace.times)
#        traceline.set_ydata(trace[0])
#        # and finally tell pylab to redraw it
#        draw()
##    print trace.times[-10:-1], trace[0][-10:-1]
##    if any((trace[0][-10:-1]) > -.01): 
##        print 'spike'
##        if AUDIO: stream.write(trace[0][-10:-1])
#    if AUDIO: stream.write(trace[0][-10:-1])
##    print trace[0], (trace[0]*1000+53.)/70.
##    if AUDIO: stream.write((trace[0]*1000+70.)/70.)
# 
#run(1*second)
#draw_gfx() # final draw to get the last bits of data in
#if PLOT:
#    ioff() # switch interactive mode off
#    show() # and wait for user to close the window before shutting down
#
#if AUDIO: stream.close()