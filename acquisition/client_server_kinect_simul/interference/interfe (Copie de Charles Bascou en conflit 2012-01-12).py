#!/usr/bin/env python
# -*- coding: utf8 -*-


import cv

import numpy as np

from socket import *
import os
import sys
from architecture import kinects
from architecture import vps


import OSC

global my_var
global sens
my_var = 0
sens =0
global my_mat
my_mat=[ [ 0 for i in range(10) ] for j in range(10) ]
global nbr_player
nbr_player =0

global my_relation
my_relation = [ [ 0 for i in range(2) ] for j in range(20) ]
global nbr_relation
nbr_relation =0

global my_group
my_group = [ [ 0 for i in range(10) ] for j in range(10) ]
global nbr_group
nbr_group =0

def show_depth():
	global my_group
	global nbr_group
	global nbr_relation
	global my_mat
	global my_relation
	global nbr_player
	global my_var
	global sens
	image = imgOut
	my_var =200
	
	font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8) #Creates a font
	cv.PutText(image,"TROPIC", (5,20),font, 255) #Draw the text

	for xyz in kinects :#draw kinect from architecture
		#print inc,  xyz['x'], xyz['y']
		cv.Rectangle(image,(int(xyz['x']-10),int (xyz['y']-10)),(int (xyz['x']+10),int (xyz['y']+10)),(100,128,0),1)
	for xyz in vps :#draw vps from architecture
		#print inc,  xyz['x'], xyz['y']
		cv.Rectangle(image,(int(xyz['x']-10),int (xyz['y']-10)),(int (xyz['x']+10),int (xyz['y']+10)),(255,255,255),1)



	image2 =cv.CloneImage(image)

	for desin in range(nbr_player):
		cv.Circle(image2,(my_mat[desin][1],my_mat[desin][2]),10,(my_var,128,0),1)
		font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8) #Creates a font
		cv.PutText(image2,str(desin), (my_mat[desin][1],my_mat[desin][2]),font, my_var)
	
	


	try :	
		Donnee, Client = PySocket.recvfrom (1024)
	except:
		detect = 0
	else :
		for nbr_ami in range (nbr_player):
			my_mat[nbr_ami][4] =0
			my_mat[nbr_ami][5] =0	
			my_mat[nbr_ami][6] =0					

		
		nbr_player=0
		#print"data =" ,Donnee 
		datasplit = Donnee.split(";")
		datasplit1 = datasplit[0].split(" o ")
		#print (datasplit1[0])
		#my_mat=[ [ 0 for i in range(20) ] for j in range(10) ]

		for nbr in datasplit1:
			#print "nbr =" ,nbr
			datasplit2 = nbr.split(" ")
			angle = int((datasplit2[0]))
			x = int((datasplit2[1]))
			y = int((datasplit2[2]))
			my_mat[nbr_player][0]=angle
			my_mat[nbr_player][1]=x
			my_mat[nbr_player][2]=y
			my_mat[nbr_player][3] +=0.1 # durée de vie

			#print "angle =", angle,"x et y =", x, y, "durée de vie", my_mat[nbr_player][3]
			nbr_player +=1
		for del_vie in range (nbr_player, 8):
			my_mat[del_vie][3] =0

		my_relation = [ [ 0 for i in range(2) ] for j in range(20) ]
		nbr_relation =0
		for test_val1 in range(nbr_player - 1):
			for test_val2 in range (test_val1+1, nbr_player) :
				if  ( ((my_mat[test_val1][1]+ 50) > my_mat[test_val2][1]) and ((my_mat[test_val1][1]- 50) < my_mat[test_val2][1]) ):
					if  ( ((my_mat[test_val1][2]+ 50) > my_mat[test_val2][2]) and ((my_mat[test_val1][2]- 50) < my_mat[test_val2][2]) ):
						#print "bingo x entre ", test_val1 ,test_val2

						x_centre = int ( (my_mat[test_val1][1] + my_mat[test_val2][1])/2)
						y_centre = int ( (my_mat[test_val1][2] + my_mat[test_val2][2])/2)
						cv.Circle(image2,(x_centre,y_centre),50,(my_var,128,0),1)
						my_relation[nbr_relation][0] = test_val1
						my_relation[nbr_relation][1] = test_val2
						nbr_relation+=1

		
		if nbr_relation != 0 :
			#print "my relation =" , my_relation
			#print "nbr de relation =", nbr_relation
			for nbr_ami in range (nbr_relation):
				my_mat[(my_relation[nbr_ami][0])][4] +=1
				my_mat[(my_relation[nbr_ami][1])][4] +=1
		total_relation = nbr_relation
		nbr_group=0
		"""	
		for group in range (nbr_relation) :
			premier_group = my_relation[0][0]
			for essai in range (1 , total_relation):

				if my_relation[essai][0] == premier_group :
					print " groupe rasseble",group, "composes de ", premier_group," et ", essai , my_relation[essai]
					my_group[group][nbr_group] = my_relation[essai][0]
					nbr_group +=1


		for reg_group in range (nbr_group):
			print "my group n =", reg_group, " constitute of ",my_group
		
		for test_rela in range (nbr_relation):
			print "le groupe n", test_rela, " contient " , my_relation[test_rela][0] , my_relation[test_rela][1]
		"""	
		for affi in range (nbr_player ):
			for nbr in range (my_mat[affi][4]) :
				if my_relation[nbr][0] == affi :
					my_mat[affi][5+nbr] =  my_relation[nbr][1]
					my_mat[my_relation[nbr][1]][4+my_mat[affi][4]] = my_relation[nbr][0]
					

			#print "numero ", affi,"angle =",my_mat[affi][0] ,"x et y =", my_mat[affi][1], my_mat[affi][2], "durée de vie", my_mat[affi][3], "nbre ami ", my_mat[affi][4], my_mat[affi][5], my_mat[affi][6]

			msg = OSC.OSCMessage() #  we reuse the same variable msg used above overwriting it
			msg.setAddress("/"+str(affi))
			msg.append(my_mat[affi])
			client.send(msg) # now we dont need to tell the client the address anymore
			#cv.Circle(image2,(x,y),10,(my_var,128,0),1)
				
			#os.system('python segmentation.py')

	for affi in range (nbr_player ):
		print "numero ", affi,"angle =",my_mat[affi][0] ,"x et y =", my_mat[affi][1], my_mat[affi][2], "durée de vie", my_mat[affi][3], "nbre ami ", my_mat[affi][4], my_mat[affi][5], my_mat[affi][6]



	#comp = comp + 1
	cv.ShowImage('Depth', image2)




cv.NamedWindow('Depth')



print('Press ESC in window to stop')

imgOut = cv.CreateImage((640,480), cv.IPL_DEPTH_8U,3)

PySocket = socket (AF_INET,SOCK_DGRAM)
PySocket.bind (('localhost',3001))
PySocket.settimeout(0.001)
client = OSC.OSCClient()
client.connect( ('127.0.0.1', 9000) ) # note that the argument is a tupple and not two arguments

while 1:
    show_depth()

    if cv.WaitKey(10) == 27:
        break
