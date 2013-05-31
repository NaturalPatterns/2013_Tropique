#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Particle-like simulations using pyglet and a ugly bitmat

"""
global my_players
my_players = [[ 0 for x in range (12) ] for y in range (10)]
global radius
radius  = 120


import sys
sys.path.append('..')
from parametres import VPs, p, volume , info_kinects,d_y, d_z,d_x, DEBUG
# Screen information
# ------------------
print d_y, d_z,d_x 
if DEBUG: sys.path.append('../network/')
#from network import VP
#vps= VP("10.42.0.102" , 7005 , 7006)
#pdata = VP("10.42.0.1" , 9005 , 9006)

import numpy as np
from math import pi , cos ,sin , tan , asin
import OSC
UDP_IP=""
UDP_PORT=3004
import socket
sock = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP
sock.bind( (UDP_IP,UDP_PORT) )
#sock.settimeout(0.5)
sock.setblocking(0)

global goodsend
goodsend = 1
UDP_IP=""
UDP_PORT=3005
testsend = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP
testsend.bind( (UDP_IP,UDP_PORT) )
#sock.settimeout(0.5)
testsend.setblocking(0)

send_UDP_IP="10.42.0.70"
send_UDP_PORT=3003

send_sock = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP
                  
client = OSC.OSCClient()
client.connect( ('10.42.0.70', 9000) ) # note that the argument is a tupple and not two arguments
                      
global rx ,ry
rx = 1
ry = 1

global freq_network
freq_network = 2
global compt_freq_network
compt_freq_network = 0

import pyglet
platform = pyglet.window.get_platform()
print "platform" , platform
display = platform.get_default_display()
print "display" , display
screens = display.get_screens()
print "screens" , screens
for i, screen in enumerate(screens):
    print 'Screen %d: %dx%d at (%d,%d)' % (i, screen.width, screen.height, screen.x, screen.y)
N_screen = len(screens) # number of screens
assert N_screen == 1 # we should be running on one screen only
  
from pyglet.window import Window
win_0 = Window(screen=screens[0], fullscreen=False, resizable=False, vsync = True)
#win_0 = Window(screen=screens[0], fullscreen=False, resizable=True, vsync = True)
#win_0.set_size(1900, 1080)
import pyglet.gl as gl

def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    gl.glEnable(gl.GL_BLEND)
    gl.glShadeModel(gl.GL_SMOOTH)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_DONT_CARE)# gl.GL_NICEST)#
    gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glDisable(gl.GL_LINE_SMOOTH)
    gl.glColor3f(1.0, 1.0, 1.0)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.gluOrtho2D(-10.0, 1810, -10.0, 1090)

win_0.on_resize = on_resize
win_0.set_visible(True)
gl.glMatrixMode(gl.GL_MODELVIEW)
gl.glLoadIdentity()

gl.glClearColor(0.0, 0.0, 0.0, 0.0)
  
gl.glShadeModel(gl.GL_FLAT)   





global my_players
my_players = [[ 0 for x in range (12) ] for y in range (10)]
print my_players
global my_ghost
my_ghost = [[ 0 for x in range (12) ] for y in range (10)]
global tour
tour =0
global nbr_player
nbr_player = 0

global caca
caca = 0

global detect
detect =250

def know(x,y):
#	print "know"
	my_players[nbr_player][3] += 1
	my_players[nbr_player][0] = x
	my_players[nbr_player][0] = x
	my_players[nbr_player][1] = y * 2
	my_players[nbr_player][4] += 1000
	#my_players[nbr_player][4] /= 2
	my_players[nbr_player][2] = 100

def unknow(x,y, z):
#	print "unknow"
	global my_players
	global nbr_player
	for place in range (5):
		if (my_players[place][4] <= 0):
			#print "good palce ", place
			my_players[place][0] = x
			my_players[place][1] = y
   			my_players[place][2] = z

			my_players[place][3] =25
			my_players[place][4] = 45
			my_players[place][11] =0
			#msg = OSC.OSCMessage()
			#msg.setAddress("/"+str(the_player))
			#msg.setAddress("/presence")
			#msg.append((place))
			#msg.append(0)
			#send_osc(msg)
			break

def test_players(x,y,z):
	global my_players
	global nbr_player
	global detect
	detect = 50
	#print "x,y",x,y

	for player in my_players:
		#player[3] += 1
		#print "for ",detect, x,y ,player[0], player[1]
		if   (((x+ detect) >= player[0]) and ((x- detect) <= player[0]) and ((y+ detect) >= player[1]) and ((y- detect) <= player[1])):
#			print "match for ",x ,y ,player
			player[0]= int ( (float (player[0]) + float (x)) / 2.0 )
			player[1]= int ( (float (player[1]) + float (y)) / 2.0 ) 

			player[2]=int ( (float (player[2]) + float (z)) / 2.0 ) 
			player[4] +=20
			#know(x,y)
			nbr_player += 1
			match = 1
			player[3] += 1
			"""
			try : player[5] = int ((float((float(player[4]) /float(player[3])))*100) )
			except :player[5] = 0
			"""
   			player[11] =0

			break
		else:
			match = 0
	if match == 0:
			#nbr_player += 1

#			print "nomatch for ", player
			if (x >= 32): unknow(x,y,z)
			nbr_player += 1
def send_osc(msg):
	try :
		#print "my osc mess=",msg
		client.send(msg) # now we dont need to tell the client the address anymore
#		client2.send(msg) # now we dont need to tell the client the address anymore
	except:
		pass #print "no osc open"

def display_player():
    global my_players
    global nbr_player
    global imaplay
    global radius
    global detect
    global tour
    global my_ghost
    #print my_players
    global caca
    global goodsend
    global freq_network
    global compt_freq_network

    str_send=""
    #col = 250
    packed = 2550
    imaplay = np.zeros((480, 640, 3), np.uint8)
    a = 0
    the_player = 0
#    print goodsend
    for player in my_players:
        player[4] -= 0.1 * player[11]
        if (player[4]<=(5)):
            player[4] = 0
            #print "mis a zero for ", player
            for x in range (6):
                player[x] = 0
			
        if (player[4] >= 25) :
            player[11] +=1

#            print"this player move up", player 
            player[4] += 1
            col =[(packed >> (8*i)) & 255 for i in range(3)]
            #print "col =",col
            if (float (player[3]) - (float (my_ghost[a][3]))) >=1 :
				life = (float (player[11]) - (float (my_ghost[a][11])) ) / (float (player[3]) - (float (my_ghost[a][3])) ) 
            else : 
				life =0
				
				for x in range (6):
					player[x] = 0
            my_dist = abs(int ( float((float(player[0])-float(my_ghost[a][0])))))
            #7 temps deplacement , 8 distance accu deplacement ,9 = temps immobile , 10 chaos sans mouvement
            if (my_dist >= 6):
                if (player[6] != 1): player[9] = 0
            else:
                if (player[6] == 1): player[9] = 0
                else: player[9] += 1

            if (my_dist >= 4):
                if (player[6]==1):
                    player[7] += 1
                    player[8] += abs(my_dist)
                else : 
                    player[7] = 0
                    player[8] = 0
                    player[6] = 1
            else:
                player[6] = 0

            if (my_dist <= 5)and (my_dist >= 2) :
                player[10] +=100
                player[10] = int(float(player[10])/2)
            else : 
                player[10] = int(float(player[10])/1.002)
            the_player +=1

            msg = OSC.OSCMessage() #  we reuse the same variable msg used above overwriting it
            #msg.setAddress("/"+str(the_player))
            msg.setAddress("/xy")
            msg.append((the_player))
            msg.append(float(float(player[0])/ (d_x*100)))
            msg.append(float(float(player[1])/(d_y*100)))
            msg.append(float(float(player[3])/1000))
#            print "the osc mess is=", msg
            batch = pyglet.graphics.Batch()

            if ( (float(float(player[0])/(d_x*100)) != 0 ) and (float(float(player[1])/(d_y*100)) != 0 ) ):
                send_osc(msg)        
                sendx = player[0]
                sendy = player[1]
                sendz = player[2]
                gl.glPointSize (16.0);
                gl.glColor4f(0.5, 0.5, 1, 1);
                makemedraw(sendx,sendy,sendz)
                pyglet.text.Label(str(the_player),font_size = 30, x=sendx- 10 , y=sendy - 20, anchor_y='bottom',color=(0, 255, 0, 255),batch=batch )

                str_send += str( int(sendx) ) + "," + str( int(sendy) ) + "," + str( int(sendz) ) + ";"
            batch.draw()
                
        packed +=55000
        a +=1
#    print goodsend
    compt_freq_network +=1
    
    if ((str_send!="") and (goodsend == 1) ):
#    if ((str_send!="")):
        str_send = str_send[0:(len(str_send) -1)]
#        print "send str=",str_send
        send_sock.sendto(str_send, (send_UDP_IP, send_UDP_PORT) )
        goodsend =0
        compt_freq_network =0

        #print "goodsend =0"

#    tour +=1
#    if (tour ==500):
#        my_ghost = np.copy(my_players)
#        print "myghost",my_ghost
#        tour = 0

    my_list=np.zeros( (10,4) )
    for  h , player1 in enumerate(my_players):
        for i,player2 in enumerate(my_players):
			find=0
			if   (((player1[0]+ radius) >= player2[0]) and ((player1[0]- radius) <= player2[0]) and ((player1[1]+ radius) >= player2[1]) and ((player1[1]- radius) <= player2[1]) and (player1[0]>=50) and (player2[0]>=50) and (i!=h)):
				#print "radius , bingo x entre ",radius, i,h ,find
				my_list[h][0]=i
				find+=1
	#print "my list =" , my_list

def drawOneLine(x1, y1, x2, y2):
  gl.glBegin(gl.GL_LINES)
  gl.glVertex2f(x1, y1)
  gl.glVertex2f(x2, y2)
  gl.glEnd()

def decors():
    gl.glColor3f(1.0, 1.0, 1.0)
    drawOneLine(0 , 0, 0 , d_y*100)
    drawOneLine(0 , d_y*100, d_x*100 , d_y*100)
    drawOneLine(d_x*100 , 0, d_x*100 , d_y*100)
    drawOneLine(0 ,0, d_x*100 , 0)
    batch = pyglet.graphics.Batch()
    for k in info_kinects :
          gl.glColor4f(0, 0, 1, 1);
          gl.glPointSize (32.0);
    
          gl.glBegin (gl.GL_POINTS);
          gl.glVertex2f(k['x']*100, k['y']*100);
          gl.glEnd();
          drawOneLine(k['x']*100 ,k['y']*100, k['x']*100 + cos (k['az'])*k['max'],k['y']*100 + sin (k['az'])*k['max'])
          pyglet.text.Label(k['address'][8:]  + str(k['port']-9998) ,font_size = 40, x=k['x']*100 - 30 , y=k['y']*100 - 30, anchor_y='bottom',color=(255, 0, 0, 255),batch=batch )
    for p in VPs:
          gl.glColor4f(0, 1, 1, 1);
          gl.glPointSize (32.0);
    
          gl.glBegin (gl.GL_POINTS);
          gl.glVertex2f(p['x']*100, p['y']*100);
          gl.glEnd();
          drawOneLine(p['x']*100 ,p['y']*100, p['cx']*100 ,p['cy']*100 )    
          pyglet.text.Label(p['address'][8:],font_size = 40, x=p['x']*100 - 30 , y=p['y']*100 - 30, anchor_y='bottom',color=(0, 0, 0, 255),batch=batch )
    batch.draw()

    gl.glFlush ()
  
def calc_angle(each, kin):
    global x,y
#    print "each=" , each
#    print "kin" , kin
    alpha = -1 * asin ( each[2] / (each[4]+0.001) )
#    print "alpha =" , alpha
    x = kin['x']*100 + cos (alpha+ kin['az']) * each[4]
    y = kin['y']*100 + sin (alpha+ kin['az']) * each[4]
    z = each[3] 
    if (z>= -100 and z<= 50) :
        pourcent = ((y / ((d_y/2)-y ))/100)*1
#        print "alpha=", alpha
#        print "pourcent  =" ,pourcent
        varz = (float(z) * (pourcent))
#        print "first varz =",varz + z
        z+=20

        z= z+ varz 

        test_players(x,y, 150-z)
        gl.glPointSize (32.0)
        gl.glColor4f(1, 0, 1, 1)


        
#        makemedraw(x,y)


#    print "x , y",x , y

#global x ,y
#x = 0
#y=0
def makemedraw(x,y,z):
    z+=1
    if z==1:
        print "erreur z=",z
    zdraw = abs(float(z))/5.0
    gl.glPointSize (zdraw);
    gl.glBegin (gl.GL_POINTS);
    gl.glVertex2f(x, y)
    gl.glEnd()
    
@win_0.event
def on_draw():
    global rx, ry
    global my_players
    global goodsend
    global my_part
    win_0.clear()
    gl.glLineWidth ( 1 )
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    decors()

    try :	
        Donnee, Client = sock.recvfrom (1024)
    except (KeyboardInterrupt):
        raise
    except:
        detect = 0
#        print "grosse erreur"
    else :
        for player in my_players:#incremente total life
            player [11] +=1

#       print"data =" ,Donnee
        #Donnee = ((angle + x + y + "o")*nbr_player)+";"
        datasplit = Donnee.split(";")
		#print "datasplit =" , datasplit
        nbr0 =0
        nbr1 = 0
        store_blob = [[ int(each2) for each2 in each.split(",") ] for each in datasplit]
        for each3 in store_blob:
#            print "alleach =",each3
            if ( int(each3[0]/2) == float(each3[0]/2.0) ) :
                for kin in info_kinects:
                    if (( kin['address'] == ('10.42.0.1'+str(int(each3[0]/2)))) and (kin['port'] == 9998) ):
#                        print 'reconise ', each3[0] , ('as 10.42.0.1'+ str(int(each3[0]/2)) ),', kin0'
                        calc_angle(each3, kin)                     
            else :
                for kin in info_kinects:
                    if (( kin['address'] == ('10.42.0.1' + str(int(each3[0]/2))) ) and (kin['port'] == 9999) ) :
#                        print 'reconise ', each3[0] , ( 'as 10.42.0.1'+ str(int(each3[0]/2))) ,', kin1'                
                        calc_angle(each3, kin) 
    display_player()
    try :	
        sendor, Client = testsend.recvfrom (1024)
    except (KeyboardInterrupt):
        raise
    except:
        pass
    else :
        goodsend = 1
    
def callback(dt):
    global rx, ry, rz 
    rx += dt
    rx %= 6.28
    ry += dt
    ry %= 6.28
#    print '%f seconds since last callback' % dt , '%f  fps' % pyglet.clock.get_fps()

    
pyglet.clock.schedule(callback)
pyglet.app.run()
print 'Goodbye'
