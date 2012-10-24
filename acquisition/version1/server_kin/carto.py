#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 11:41:24 2012

@author: BIOGENE
"""

import sys
sys.path.append('../../../projection/')

import cv2
import numpy as np
import cv

import socket

import math 
import OSC
from parametres import info_kinects

img = np.zeros((480, 600, 3), np.uint8)
#cv2.namedWindow('nb',cv.CV_WINDOW_NORMAL)
##cv2.setWindowProperty('nb',cv.CV_WINDOW_NORMAL,cv.CV_WINDOW_FULLSCREEN)
#cv2.setWindowProperty('nb',cv.CV_WINDOW_AUTOSIZE,cv.CV_WINDOW_AUTOSIZE)
#
#cv2.namedWindow('record',cv.CV_WINDOW_NORMAL)
##cv2.setWindowProperty('nb',cv.CV_WINDOW_NORMAL,cv.CV_WINDOW_FULLSCREEN)
#cv2.setWindowProperty('record',cv.CV_WINDOW_AUTOSIZE,cv.CV_WINDOW_AUTOSIZE)
#cv2.cv.MoveWindow('record',1,1)
##cv2.cv.ResizeWindow('record',800,240)

cv2.namedWindow('player',cv.CV_WINDOW_NORMAL)
#cv2.setWindowProperty('nb',cv.CV_WINDOW_NORMAL,cv.CV_WINDOW_FULLSCREEN)
#cv2.setWindowProperty('player',cv.CV_WINDOW_NORMAL,cv.CV_WINDOW_FULLSCREEN)
cv2.setWindowProperty('player',cv.CV_WINDOW_AUTOSIZE,cv.CV_WINDOW_AUTOSIZE)
cv2.cv.MoveWindow('player',1,400)

global radius
radius  = 100

def up_radius(thevar):
	global radius
	radius = thevar
	print "update", radius
"""
global x
global y
global z
"""
global angle
global lastz
global zm
zm=0
lastz=0
angle =0
"""
x=100
y=100
z=100
"""
global color
color =(255,255,255)
coef_x =0.5
coef_y = 0.5

UDP_IP=""
UDP_PORT=3004

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


#print "UDP target IP:", send_UDP_IP
#print "UDP target port:", send_UDP_PORT


send_sock = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP

client = OSC.OSCClient()
client.connect( ('10.42.0.70', 9000) ) # note that the argument is a tupple and not two arguments

client2 = OSC.OSCClient()
client2.connect( ('10.42.0.1', 9000) ) # note that the argument is a tupple and not two arguments

global imagen
imagen = np.zeros((480, 640, 3), np.uint8)
"""cv2.rectangle(imagen,(50,50),(500,400),(255,255),2)
cv2.circle(imagen,(x,z),1,color,3)
img2 = np.zeros((480, 640, 3), np.uint8)
img2=np.copy(imagen)
"""
global imaplay
imaplay = np.zeros((480, 640, 3), np.uint8)

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
detect =20

def know(x,y):
#	print "know"
	my_players[nbr_player][3] += 1
	my_players[nbr_player][0] = x
	my_players[nbr_player][1] = y * 2
	my_players[nbr_player][4] += 10
	#my_players[nbr_player][4] /= 2
	my_players[nbr_player][2] = 100

def unknow(x,y):
#	print "unknow"
	global my_players
	global nbr_player
	for place in range (5):
		if (my_players[place][4] <= 0):
			#print "good palce ", place
			my_players[place][0] = x
			my_players[place][1] = y
			my_players[place][3] =5
			my_players[place][4] = 25
			my_players[place][11] =10
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
	detect = 28
	#print "x,y",x,y

	for player in my_players:
		#player[3] += 1
		#print "for ",detect, x,y ,player[0], player[1]
		if   (((x+ detect) >= player[0]) and ((x- detect) <= player[0]) and ((y+ detect) >= player[1]) and ((y- detect) <= player[1])):
			#print "match for ",x ,y ,player

			player[0]= int ( (float (player[0]) + float (x)) / 2.0 )
			player[1]= int ( (float (player[1]) + float (y)) / 2.0 ) 

			player[2]=int ( (float (player[2]) + float (z)) / 2.0 ) 
			player[4] +=2
			#know(x,y)
			nbr_player += 1
			match = 1
			player[3] += 1
			"""
			try : player[5] = int ((float((float(player[4]) /float(player[3])))*100) )
			except :player[5] = 0
			"""
			break
		else:
			match = 0

	

	if match == 0:
			#nbr_player += 1

#			print "nomatch for ", player
			if (x >= 32): unknow(x,y)
			nbr_player += 1
def send_osc(msg):
	try :
		#print "my osc mess=",msg
		client.send(msg) # now we dont need to tell the client the address anymore
		client2.send(msg) # now we dont need to tell the client the address anymore
	except:
		#print "no osc open"
		rien =  0		

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
    str_send=""
    #col = 250
    packed = 2550
    imaplay = np.zeros((480, 640, 3), np.uint8)
    a = 0
    the_player = 0
    for player in my_players:
        player[4] -= 1 
        if (player[4]<=(5)):
            player[4] = 0
            #print "mis a zero for ", player
            for x in range (6):
                player[x] = 0
			
        if (player[4] >= 25) :
            player[4] += 1
            col =[(packed >> (8*i)) & 255 for i in range(3)]
            #print "col =",col
            if (float (player[3]) - (float (my_ghost[a][3]))) >=1 :
				life = (float (player[11]) - (float (my_ghost[a][11])) ) / (float (player[3]) - (float (my_ghost[a][3])) ) 
            else : 
				life =0
				
				for x in range (6):
					player[x] = 0
            cv2.rectangle(imaplay,(50,50),(590,430) , (255,255,255) , 5)
            cv2.circle(imaplay,(player[0],player[1]),5,col,10)
            cv2.circle(imaplay,(50 , 50),15,(255,255,255),10)

   
            #cv2.circle(imaplay,(player[0],player[1]),detect*2,(128,180,225),1)
            #cv2.circle(imaplay,(player[0],player[1]),int ( (1/((player[2]+0.01)*0.00022) / ((player[1]/1000.0)+0.001) ) /10),(128,180,225),1)
            #cv2.putText(imaplay,str(player[3]), (player[0],player[1] - 10), 1 , 1, (255,255,255), 1 , 8)
            #cv2.putText(imaplay,str( int(100 * life)), (player[0] + 10,player[1]), 1 , 1, (255,255,255), 1 , 8)
            cv2.putText(imaplay,str(player[0]), (player[0],player[1] - 10), 1 , 1, (255,255,255), 1 , 8)
            cv2.putText(imaplay,str(200 + (640 - (player[0]))), (player[0] + 10,player[1]), 1 , 1, (255,255,255), 1 , 8)
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
            msg.append(float(float(player[0])/640))
            msg.append(float(float(player[1])/480))
            msg.append(float(float(player[3])/1000))
#            print "the osc mess is=", msg
            if ( (float(float(player[0])/640) != 0 ) and (float(float(player[1])/480) != 0 ) ):
                send_osc(msg)

                #str_send += str(player[0]) + "," + str(player[1]) + "," + str(player[2]) + "," + str(player[3]) + "," + str(player[4]) + "," + str(player[5]) + "," + str(player[6]) + "," + str(player[7]) + "," + str(player[8]) + "," + str(player[9]) +";"
                #sendx = 350 + ( (640 - (player[0]))* 1.2)
                #sendy = (350 - player[1])* -1.5
                #sendz = (player[2]) -50
#			sendx = ( 350 + ( (640 - (player[0]))* 1.2) ) 
#   			sendx = ( 350 + ( ((player[0]))* 1.2) ) 
#-----------------parametre vp a 8,60m / calibration a 0/430/130 (fond de salle)
#                sendx = abs (( ( ((player[0]))* 2.2) )  - 130)
#                sendy = abs ((390 - player[1])* 3) 
#                sendz = ( (1/((player[2]+0.01)*0.00022) / ((player[1]/1000.0)+0.001) ) / 2) - 50
#                sendz = 140  - ( (player[2] * 2) )
#-------------------------------------------------------
        
                sendx = abs (( ( ((player[0]))* 2.2) )  - 190)
                if (sendx>= 1500) : sendx=1500
#                sendy = abs ((390 - player[1])* 3) 
                sendy = abs ((390 - player[1])* 3) 

#                sendz = ( (1/((player[2]+0.01)*0.00022) / ((player[1]/1000.0)+0.001) ) / 2) - 50
                sendz = 200  - ( (player[2] * 2) )
#               sendz = 200

                str_send += str( int(sendx) ) + "," + str( int(sendy) ) + "," + str( int(sendz) ) + ";"
		
        packed +=55000
        a +=1
	
    if ((str_send != "" ) and (goodsend == 1 ) ):
        str_send = str_send[0:(len(str_send) -1)]
#        print "send str=",str_send
        send_sock.sendto(str_send, (send_UDP_IP, send_UDP_PORT) )
        goodsend =0
        #print "goodsend =0"

    tour +=1
    if (tour ==50):
        my_ghost = np.copy(my_players)
        #print "myghost",my_ghost
        tour = 0

    my_list=np.zeros( (10,4) )
    for  h , player1 in enumerate(my_players):
        for i,player2 in enumerate(my_players):
			find=0
			if   (((player1[0]+ radius) >= player2[0]) and ((player1[0]- radius) <= player2[0]) and ((player1[1]+ radius) >= player2[1]) and ((player1[1]- radius) <= player2[1]) and (player1[0]>=50) and (player2[0]>=50) and (i!=h)):
				#print "radius , bingo x entre ",radius, i,h ,find
				my_list[h][0]=i
				find+=1
	#print "my list =" , my_list
	"""			
			msg = OSC.OSCMessage()
			#msg.setAddress("/"+str(the_player))
			msg.setAddress("/len")
			msg.append(float(float(player[3])/1000))
			msg.append(float(float(player[7])/1000))
			msg.append(float(float(player[9])/1000))
			send_osc(msg)
	"""
	

	"""
	for test_val1 in range(nbr_player - 1):
		for test_val2 in range (test_val1+1, nbr_player) :
			if  (((my_players[test_val1][0]+ radius) > my_players[test_val2][0]) and ((my_players[test_val1][0]- radius) < my_players[test_val2][0]) ):
				if  (( (my_players[test_val1][1]+ radius) > my_players[test_val2][1]) and ((my_players[test_val1][1]- radius) < my_players[test_val2][1]) ):
					print "bingo x entre ", test_val1 ,test_val2
					
					x_centre = int ( (my_players[test_val1][0] + my_players[test_val2][0])/2)
					y_centre = int ( (my_players[test_val1][1] + my_players[test_val2][1])/2)
					cv2.circle(imaplay,(x_centre,y_centre),radius,(128,180,225),1)

	"""
    cv2.imshow('player', imaplay)

def calc_angle(each, x_pos , y_pos , z_pos , azimut):

    coord_x = float(int(each[2])) - 320

    coord_z= 1.0 / ((int(each[4])) * -0.0030711016 + 3.3309495161)
    zm = (int(each[4]))
    coord_x /= (5/(coord_z) )
    coord_y = each[3]
    coord_y /= ((coord_z) )

    coord_z*=100
    try :
        angle = ( math.asin(coord_x/coord_z)) + azimut		
    except ValueError:
        print"bad"
    else:
        #print "x1z1  angle=", coord_x, int (coord_z), angle
        if y_pos == 1 :
            z= 50 + int((math.cos (angle) * coord_z) *coef_y)
            x=640 - ( x_pos+int ((math.sin (angle) * coord_z) * coef_x))

        else :
            z= 430 - int((math.cos (angle) * coord_z) *coef_y)
            x= ( x_pos+int ((math.sin (angle) * coord_z) * coef_x))

            
#        coord_y -= z /5 # a reprendre  car IMPORTANT a gerer importance de la taille en fonction de la distance au VP
        #y = each[3]
        y = coord_y
        #print "x2z2  angle=", x, z, angle
        test_players(x,z, y)


cv2.createTrackbar( "radius", 'player', 50, 100, up_radius )
while 1:
    img2 = np.zeros((480, 640, 3), np.uint8)
    nbr_player = 0
    try :	
        Donnee, Client = sock.recvfrom (1024)

    except (KeyboardInterrupt):
        raise
    except:
        detect = 0
    else :
        for player in my_players:#incremente total life
            player [11] +=1

        #print"data =" ,Donnee 
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
                        calc_angle(each3, kin['x'] , kin['y'] , kin['z'] , kin['az'])                     
            else :
                for kin in info_kinects:
                    if (( kin['address'] == ('10.42.0.1' + str(int(each3[0]/2))) ) and (kin['port'] == 9999) ) :
#                        print 'reconise ', each3[0] , ( 'as 10.42.0.1'+ str(int(each3[0]/2))) ,', kin1'                
                        calc_angle(each3, kin['x'] , kin['y'] , kin['z'] , kin['az']) 

     
#        #print "each3 ", each3
#            localz= int(each3[4])
#            if int(each3[0]) == 0: #10.42.43.10
#                calc_angle(each3) 
#            if int(each3[0]) == 1: #10.42.43.10
#                calc_angle(each3)                                                          
#            if int(each3[0]) == 2: #10.42.43.11
#                calc_angle(each3)                                                          
#            if int(each3[0]) == 3: #10.42.43.12
#                calc_angle(each3)   
#            if int(each3[0]) == 4: #10.42.43.12
#                calc_angle(each3)                                                       
#        #cv2.imshow('nb', img2)
#        #cv2.imshow('record', imagen)
#        #print "my player = ",nbr_player, my_players
        display_player()
	try :	
		sendor, Client = testsend.recvfrom (1024)

	except (KeyboardInterrupt):
		raise
	except:
		pass
	else :
		goodsend = 1

	if cv.WaitKey(10) == 27:
		break

