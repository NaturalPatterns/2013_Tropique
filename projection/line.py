#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Particle-like simulations using pyglet and a ugly bitmat

"""
DEBUG = False
#DEBUG = True

# Parameters
# ----------
#downscale = 4 # to debug
downscale = 1 # the real stuff / beware the segmentation fault
# x, l’axe long, y l’axe transversal, z la hauteur
#N_Y, N_Z = int(screen.width//downscale), int(screen.height//downscale) # size of the simulation grid
# ---------
# Scenarios
# ---------
scenario = 'calibration'
#scenario = 'fan'
#scenario = '2fan'
#scenario = 'rotating-circle'
#scenario = 'euler'#
scenario = 'leapfrog'#

# Screen information
# ------------------
from parametres import VPs, volume, p

import pyglet
#pyglet.options['darwin_cocoa'] = True
platform = pyglet.window.get_platform()
print "platform" , platform
display = platform.get_default_display()
print "display" , display
screens = display.get_screens()
print "screens" , screens
for i, screen in enumerate(screens):
    print 'Screen %d: %dx%d at (%d,%d)' % (i,screen.width, screen.height, screen.x, screen.y)
#screen   = screens[0]
N_screen = len(screens) # number of screens
N_screen = 1 # uncomment to force display on one screen only
#N_screen = 2 # uncomment to force display on two screens at most only
if N_screen < len(screens): screens = screens[:N_screen]

if (N_screen>1): do_sock=True
else: do_sock=False
#do_sock=True

if do_sock:
    import socket 
    UDP_IP=""
    UDP_PORT=3003
    print "UDP my port:", UDP_PORT
    sock = socket.socket( socket.AF_INET,socket.SOCK_DGRAM ) # UDP
    sock.bind( (UDP_IP,UDP_PORT) )
    #sock.settimeout(0)
    sock.setblocking(0)
    send_UDP_IP="10.42.43.20"
    send_UDP_PORT=3005
    print "UDP target IP:", send_UDP_IP
    print "UDP target port:", send_UDP_PORT
    send_sock = socket.socket( socket.AF_INET,socket.SOCK_DGRAM ) # UDP
    global para_data
    para_data=[1 , 10, 50, 350, 5 ] # TODO : decrire a quoi ca correspond?
    
    def read_sock():
        global para_data
        try :	
            Donnee, Client = sock.recvfrom (128)
        except (KeyboardInterrupt):
            raise
        except:
           pass # detect = 0
        else :
#            print"data =" ,Donnee , Client
            #Donnee = ( x + y + z +";")*nbr_player)
            datasplit = Donnee.split(";")
    #	print "datasplit =" , datasplit
            if (Client[0] == "10.42.43.1"): 
                store_blob = [[ int(each2) for each2 in each.split(" ") ] for each in datasplit[:len(datasplit)-1]]
                store_blob[0][1]+=200
                store_blob[0][2]+=200
                para_data = store_blob[0][3:]
#                print "the paradata are",para_data
    
            else: 
                store_blob = [[ int(each2) for each2 in each.split(",") ] for each in datasplit]
                for all in store_blob:
                    all+=para_data
    
    #	store_blob = [ int(each2) for each2 in datasplit[0].split(" ") ]
            return store_blob

else:
    positions = None    


# Window information
# ------------------
from pyglet.window import Window
wins = []
for i_screen, screen in enumerate(screens):
    if ((N_screen==1) and (i_screen==0)) or ((N_screen>1) and (i_screen>0)): 
#        print ((N_screen==1) and (i_screen==0))
        wins.append(Window(screen=screens[i_screen], fullscreen=not((N_screen==1) and (i_screen==0)), resizable=((N_screen==1) and (i_screen==0)) ))#((N_screen==1) and (i_screen==0))))
#        print('OpenGL version:', wins[i_screen].context.get_info().get_version())
#        print('OpenGL 3.2 support:', wins[i_screen].context.get_info().have_version(3, 2))
#        icon1 = pyglet.image.load('16x16.png')
#        icon2 = pyglet.image.load('32x32.png')
#        window.set_icon(icon1, icon2)
import pyglet.gl as gl
from pyglet.gl.glu import gluLookAt

def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    gl.glEnable(gl.GL_BLEND)
    gl.glShadeModel(gl.GL_SMOOTH)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_DONT_CARE)# gl.GL_NICEST)#
    gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glDisable(gl.GL_LINE_SMOOTH)
    gl.glColor3f(1.0, 1.0, 1.0)
#
#def on_draw():
#    global s, i_win
#try:
#    if ((N_screen==1) and (i_win==0)) or ((N_screen>1) and (i_win==1)): 
##        print i_win	 
#        s.do_scenario()
#    win.clear()
#    pyglet.graphics.draw(2*s.N, gl.GL_LINES, ('v3f', s.particles[0:6, :].T.ravel().tolist()))


for i_win, win in enumerate(wins):
    win.on_resize = on_resize
    win.set_visible(True)
    win.set_mouse_visible(False)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    gl.gluPerspective(VPs[i_win]['foc'], 1.0*win.width/win.height, VPs[i_win]['pc_min'], VPs[i_win]['pc_max'])
    gluLookAt(VPs[i_win]['x'], VPs[i_win]['y'], VPs[i_win]['z'],
          VPs[i_win]['cx'], VPs[i_win]['cy'], VPs[i_win]['cz'],
          0., 0, 1.0)
#    win.on_draw = on_draw

from scenarios import Scenario
s = Scenario(p['N'], scenario, volume, VPs, p)

#global mytest
#mytest=[]
#for testplay in range (9):
#    mytest.append(Scenario(p['N'], scenario, volume, VPs, p))

try:
    caca
    import pylab
    fig = pylab.figure(1)
#    AX = fig.add_subplot(111)
    pylab.ion()
    # turn interactive mode on for dynamic updates.  If you aren't in interactive mode, you'll need to use a GUI event handler/timer.
    from matplotlib.widgets import Slider
    ax, value = [], []
    n_key = len(s.p.keys())*1.
#    print s.p.keys()
    for i_key, key in enumerate(s.p.keys()):
#        print [0.1, 0.05+i_key/(n_key+1)*.9, 0.9, 0.05]
        ax.append(fig.add_axes([0.15, 0.05+i_key/(n_key-1)*.9, 0.6, 0.05], axisbg='lightgoldenrodyellow'))
        value.append(Slider(ax[i_key], key, 0., s.p[key]*10, valinit=s.p[key]))
    def update(val):
        for i_key, key in enumerate(s.p.keys()):        
            s.p[key]= value[i_key].val    
            # print key, s.p[key], value[i_key].val
    for i_key, key in enumerate(s.p.keys()): value[i_key].on_changed(update)
    
    fig.show(block=False) # il faut pylab.ion() pour pas avoir de blocage
    
except Exception, e:
    print('problem while importing sliders ! Error = ', e)

##if DEBUG: fps_display = pyglet.clock.ClockDisplay(color=(1., 1., 1., 1.))
from numpy import cos, pi
win_0=wins[0]
@win_0.event
def on_draw():
    global s
    
    if do_sock:
        send_sock.sendto("1", (send_UDP_IP, send_UDP_PORT) )
        positions = read_sock() # TODO: c'est bien une liste de coordonnées [x, y, z] ?
        
        # TODO: ces hacks permettent d'éviter un trou dans la captation: mais ça doit aller dans les scripts de captation justement...
#    #    all_player=[[100,200,200]]
#    #        print 'all1&_player =', all_player
#        if not(all_player_==None):
#            all_player = all_player_
##        try :
#            if not(all_player==None):
#                for i_player, player in enumerate(all_player) :
#                    #            print player
#                    #                gl.glLineWidth((player[5]/10)+1)
#                    mytest[i_player].do_scenario(positions=[float(player[0])/100.0,float(player[1])/100.0,float(player[2])/100.0])
#                    print "player n°",i_player, ':', float(player[0])/100.0,float(player[1])/100.0,float(player[2])/100.0 
##        except :
##            pass
    else:
        # HACK pour simuler ROGER:
        positions = []
#        positions = [[s.center[0], s.center[1], s.center[2]]] # une personne fixe
        T = 20.
        positions.append([s.center[0], s.center[1] * (1 - .5*cos(2*pi*s.t/T)), 1.5*s.center[2]]) # une personne dans un mouvement circulaire (elipse)
        positions.append([s.center[0], s.center[1] * (1 + .5*cos(2*pi*s.t/T)), 0.5*s.center[2]]) # une autre personne dans un mouvement en phase
#    print positions
    s.do_scenario(positions=positions)
    
    win.clear()
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    gl.gluPerspective(VPs[0]['foc'], 1.0*win_0.width/win_0.height, 
                      VPs[0]['pc_min'], VPs[0]['pc_max'])
    gluLookAt(VPs[0]['x'], VPs[0]['y'], VPs[0]['z'],
          VPs[0]['cx'], VPs[0]['cy'], VPs[0]['cz'], 0., 0, 1.0)
    #    gl.glColor3f(1.0, 0., 0.)
    #    gl.glPointSize (10)
    
    pyglet.graphics.draw(2*s.N, gl.GL_LINES, ('v3f', s.particles[0:6, :].T.ravel().tolist()))
#    if do_sock:
#        if not(all_player==None):
#            for i_player, player in enumerate(all_player)  :
#                pyglet.graphics.draw(2*mytest[i_player].N, gl.GL_LINES, ('v3f', mytest[i_player].particles[0:6, :].T.ravel().tolist()))
##        except :
##            pass
    

#    if DEBUG: fps_display.draw()

if N_screen>1:
    win_1=wins[1]
    @win_1.event
    def on_draw():
        win.clear()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.gluPerspective(VPs[1]['foc'], 1.0*win_1.width/win_1.height, 
                      VPs[1]['pc_min'], VPs[1]['pc_max'])
        gluLookAt(VPs[1]['x'], VPs[1]['y'], VPs[1]['z'],
          VPs[1]['cx'], VPs[1]['cy'], VPs[1]['cz'], 0., 0, 1.0)
#        gl.glColor3f(0., 1.0, 0.)
#        gl.glPointSize (10)
#        pyglet.graphics.draw(2*s.N, gl.GL_LINES, ('v3f', s.particles[0:6, :].T.ravel().tolist()))
        if do_sock:
            if not(all_player==None):
                for i_player, player in enumerate(all_player)  :
                    pyglet.graphics.draw(2*mytest[i_player].N, gl.GL_LINES, ('v3f', mytest[i_player].particles[0:6, :].T.ravel().tolist()))

if N_screen>2:
    win_2=wins[2]
    @win_2.event
    def on_draw():
        win.clear()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.gluPerspective(VPs[2]['foc'], 1.0*win_2.width/win_2.height, 
                      VPs[2]['pc_min'], VPs[2]['pc_max'])
        gluLookAt(VPs[2]['x'], VPs[2]['y'], VPs[2]['z'],
          VPs[2]['cx'], VPs[2]['cy'], VPs[2]['cz'], 0., 0, 1.0)
#        gl.glColor3f(0., 0., 1.0)
#        gl.glPointSize (10)
#        pyglet.graphics.draw(2*s.N, gl.GL_LINES, ('v3f', s.particles[0:6, :].T.ravel().tolist()))
        if do_sock:
            if not(all_player==None):
                for i_player, player in enumerate(all_player)  :
                    pyglet.graphics.draw(2*mytest[i_player].N, gl.GL_LINES, ('v3f', mytest[i_player].particles[0:6, :].T.ravel().tolist()))


   
#win_3=wins[3]
#@win_3.event
#def on_draw():
#    win.clear()
#    gl.glColor3f(1., 1., 1.)
#    pyglet.graphics.draw(s.N, gl.GL_POINTS, ('v3f', s.particles[0:3, :].T.ravel().tolist()))

def callback(dt):
    global do_sock
    try :
        if DEBUG: print '%f seconds since last callback' % dt , '%f  fps' % pyglet.clock.get_fps()
    except :
        pass

    
#dt = 1./40 # interval between 2 captations
#pyglet.clock.schedule_interval(callback, dt)
pyglet.clock.schedule(callback)
#pyglet.clock.schedule(lambda dt: None)
pyglet.app.run()
print 'Goodbye'
