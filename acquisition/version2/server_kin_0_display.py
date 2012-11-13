#!/usr/bin/env python
# -*- coding: utf8 -*-
import freenect
import cv2
import cv
import frame_convert
import numpy as np

import socket
import string

import sys
from glob import glob
import itertools as it
import math

import socket
import fcntl
import struct
global my_thresholdarray
#sys.path.append('../../../projection/')
#from parametres import info_kinects

print('Press ESC in window to stop')

global server_kin
server_kin = 0
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
    
#my_ip = get_ip_address('eth0')
#print "my ip is =", my_ip
#global my_number  
#my_number= (int(my_ip[len(my_ip)-1])*2)+ server_kin
#string_name= str(my_ip) +","+str(my_number)

string_name="fenetre"
my_number = 0


print('Press ESC in window to stop')

cv2.namedWindow(string_name,cv.CV_WINDOW_NORMAL)
cv2.cv.MoveWindow(string_name,1,600)
cv2.cv.ResizeWindow(string_name,400,400)

threshold = 400
#current_depth = 495
level = 3

#for kin in info_kinects:
#    if ( (kin['address'] == my_ip) and (kin['port'] == 9998+server_kin) )  :
#        current_depth = kin['max']

UDP_IP="10.42.0.1"
UDP_PORT=5005

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sock = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP


PySocket = socket.socket (socket.AF_INET,socket.SOCK_DGRAM)
PySocket.bind (('',9998 + server_kin))
PySocket.settimeout(0.001)

global good_z


def change_threshold(value):
    global threshold
#    print int( ((1.0/(float(value)/100))-3.33) / -0.003071)
    threshold = value
global img_moy
img_moy = np.zeros((480, 640), np.uint8)

def get_depth0():
    print "ANEWROUND"
    global my_thresholdarray
    global img_moy

    global threshold
    global current_depth
    valu_array=[0 , 0 , 0 , 0, 0, 0]

    dx,dy =0,0
    black, white = 0, 255
    img2 = np.zeros((480, 640), np.uint8)
    my_depth, timestamp = freenect.sync_get_depth(server_kin)
    data = my_depth
    global image_depth, i_frame, depth_hist, learn, record_list
    my_array = my_depth
    cv2.imshow("0", my_depth.astype(np.uint8))

    for nbr_test in range (0,my_thresholdarray.shape[0]):
       my_array[my_thresholdarray[nbr_test][0]  ] = my_array[my_thresholdarray[nbr_test][0]] * np.less_equal( my_array[my_thresholdarray[nbr_test][0]],  my_thresholdarray[nbr_test][1])

#    my_array2 = 255 * np.logical_and(my_array >= current_depth - threshold,my_array <= current_depth + threshold)
    my_array2 = my_array * np.logical_and(my_array >= 0,my_array <= int( ((1.0/(float(threshold)/100))-3.33) / -0.003071))
#    print "threshold=",threshold
    cv2.imshow("1", my_array.astype(np.uint8))

    my_array2 = my_array2.astype(np.uint8)
    cv2.imshow("2", my_array2.astype(np.uint8))

    img = my_array2

    img2= my_array2  
    h, w = img2.shape[:2]
    levels = 3
    contours0, hierarchy = cv2.findContours( img2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cv2.approxPolyDP(cnt, levels, True) for cnt in contours0]
#    send_string = str("")
    def update(levels):
        vis = np.zeros((h, w, 3), np.uint8)
        nbr = 0
        global send_string
        send_string = str("")
        global good_z
        for cnt in contours:
            if (len(cnt)>8) and (cv2.contourArea(cnt) > 2000):
                centre = cv2.minAreaRect(cnt)
                area = cv2.contourArea(cnt)
                a= 0
                x_moy = 0
                y_moy=0
                x_max = 0
                x_min = 640
                y_max = 0
                y_min = 480
                for i in cnt:
                    #print "my i =",i
                    x= i[0][0]
                    y=i[0][1]
                    if (x > x_max):
                        x_max = x
                    if (x < x_min):
                        x_min = x
                    if (y > y_max):
                        y_max = y
                    if (y < y_min):
                        y_min = y
                    x_moy += x
                    y_moy+= y
                    a +=1
                    #print "x , y = " ,x ,y
                    cv2.circle(vis,(x,y),10,255,3)
    
                #x_moy = (int(centre[0][0]))
                #y_moy = (int(centre[0][1]))
                x_moy = int((x_min+x_max)/2)
                y_moy = int((y_min+y_max)/2)
                my_z = 0
                a = 0
                for i in (range (3)):
                    for k in (range (3)):
                        try :
                            if ( (data [(y_moy-1)+i][(x_moy-1)+k])<= 1024 ):
                                my_z += data [(y_moy-1)+i][(x_moy-1)+k]
                                poor_data =0
                                a+=1
    #                                    print "good" , data [(y_moy-1)+i][(x_moy-1)+k]
                            else:
    #                                    print "the goodz is bad " , (data [(y_moy-1)+i][(x_moy-1)+k])
                                pass
                        except:
    #                                print "bad data"
                            poor_data =1
                            
                global good_z      
                if a!=0:
                    my_z =int (my_z/a)
                    good_z = my_z
    #                    print "z , my_z = " , data [y_moy][x_moy], good_z
                    cv2.circle(vis,(x_moy,y_moy),25,(255,255),3)
                    cv2.circle(vis,(int(centre[0][0]),(int(centre[0][1]))) ,25,(255,255,255),3)
                    cv2.circle(vis,(int((x_min+x_max)/2),int((y_min+y_max)/2)) ,25,(0,255,255),3)
     
                    valu_array[0]=my_number
                    valu_array[1]=nbr
                    valu_array[2]= x_moy
                    valu_array[3]= y_min
#                    valu_array[4]=good_z
                    valu_array[4]= int(( 1.0/( (float(good_z)* -0.0030711016 + 3.3309495161)))*100)
                    valu_array[5]=100 
                    nbr +=1
                    for val in valu_array:
                        send_string += str (val) + ","
        #			print "my len =" 
                    print send_string
                    send_string = send_string[0:(len(send_string) -1)]
                    send_string += ";"
                else:
                    cv2.circle(vis,(x_moy,y_moy),25,(0,125,255),3)
                        



#        levels = 5
        cv2.drawContours( vis, contours, (-1, 3)[levels <= 0], (128,255,255), 3, cv2.CV_AA, hierarchy, abs(levels) )
	vis = cv2.resize(vis, (320,240))
        cv2.imshow(string_name, vis)
    update(levels)
    cv2.createTrackbar( "depth", string_name, threshold, 500, change_threshold ) 
    print "sendstring",send_string
    try :	
        Donnee, Client = PySocket.recvfrom (1024)
        print Donnee
    except :
         pass#		print "no need of data"
    else :
         if Donnee == "data":
             PySocket.sendto (send_string,Client)
             print timestamp

"""
    def update(levels):
        vis = np.zeros((h, w, 3), np.uint8)
        nbr = 0
    	send_string = str("")
        for cnt in contours:
 		global good_z
	        if (len(cnt)>8) and (cv2.contourArea(cnt) > 2000):
#		    print "len cnt ok contourArea ok"
                    centre = cv2.minAreaRect(cnt)
                    area = cv2.contourArea(cnt)
		    
                    a= 0
                    x_moy = 0
                    y_moy=0
		    x_max = 0
                    x_min = 640
                    y_max = 0
		    y_min = 480
                    for i in cnt:
                        #print "my i =",i
                        x= i[0][0]
                        y=i[0][1]
			if (x > x_max):
                            x_max = x
			if (x < x_min):
			    x_min = x
			if (y > y_max):
                            y_max = y
			if (y < y_min):
			    y_min = y
                        x_moy += x
                        y_moy+= y
                        a +=1
                        #print "x , y = " ,x ,y
	                cv2.circle(vis,(x,y),10,255,3)

                    #x_moy = (int(centre[0][0]))
                    #y_moy = (int(centre[0][1]))
                    x_moy = int((x_min+x_max)/2)
                    y_moy = int((y_min+y_max)/2)
                    my_z = 0
                    a = 0
                    for i in (range (3)):
                        for k in (range (3)):
                            try :
                                if ( (data [(y_moy-1)+i][(x_moy-1)+k])<= 1024 ):
                                    my_z += data [(y_moy-1)+i][(x_moy-1)+k]
                                    poor_data =0
                                    a+=1
#                                    print "good" , data [(y_moy-1)+i][(x_moy-1)+k]
                                else:
#                                    print "the goodz is bad " , (data [(y_moy-1)+i][(x_moy-1)+k])
                                    pass
                            except:
#                                print "bad data"
                                poor_data =1
                                
                    global good_z      
                    if a!=0:
                        my_z =int (my_z/a)
			good_z = my_z
                    #print "z , my_z = " , data [y_moy][x_moy], good_z
	            	cv2.circle(vis,(x_moy,y_moy),25,(255,255),3)
	            	cv2.circle(vis,(int(centre[0][0]),(int(centre[0][1]))) ,25,(255,255,255),3)
	            	cv2.circle(vis,(int((x_min+x_max)/2),int((y_min+y_max)/2)) ,25,(0,255,255),3)
 
                    	valu_array[0]=my_number
                     
		   	valu_array[1]=nbr
                    	valu_array[2]= x_moy
                    	valu_array[3]= y_min
                   	valu_array[4]=good_z
                    	valu_array[5]=100 
                    	send_array = str(valu_array)
                    	sock.sendto(send_array, (UDP_IP, UDP_PORT) )
#		   	print "people dtect , area ,x1,z1  = ",nbr, area, x_moy,good_z       

                    	nbr +=1
			for val in valu_array:
       
               print "the calcul val =",val
               send_string += str (val) + ","
#			print "my len =" 
			send_string = send_string[0:(len(send_string) -1)]
			send_string += ";"
		    else:
                        cv2.circle(vis,(x_moy,y_moy),25,(0,125,255),3)

#        levels = 5
        cv2.drawContours( vis, contours, (-1, 3)[levels <= 0], (128,255,255), 3, cv2.CV_AA, hierarchy, abs(levels) )
	vis = cv2.resize(vis, (320,240))
        cv2.imshow(string_name, vis)
    update(levels)
    #cv2.createTrackbar( "levels+3", "contours", level, 7, updated )
    cv2.createTrackbar( "depth", string_name, threshold, 500, change_threshold )  
    try :	
        Donnee, Client = PySocket.recvfrom (1024)
        print Donnee
    except :
         pass#		print "no need of data"
    else :
         if Donnee == "data":
             PySocket.sendto (send_string,Client)
             print timestamp
    #cv2.imshow('nb', img2)
    #cv.ShowImage('Video1', img)
"""




"""
cv.NamedWindow('Video1')
cv.CreateTrackbar('threshold', 'Video1', threshold,     500,  change_threshold)
cv.CreateTrackbar('depth',     'Video1', current_depth, 2048, change_depth)
cv2.createTrackbar( "levels+3", "contours", 3, 7, updated )
"""

def make_my_thresholdarray():

    threshold = 500
    current_depth = 500
    global my_thresholdarray

    valu_array=[0 , 0 , 0 , 0, 0, 0]

    dx,dy =0,0
    black, white = 0, 255
    img_moy = np.zeros((480, 640), np.uint8)
    for long_test in range (10):
        the_depth, timestamp = freenect.sync_get_depth(0)
        data = the_depth
        global image_depth, i_frame, depth_hist, learn, record_list
        my_array = the_depth
        
        #print "my dim0 = ",my_array_split[2].shape
    #    my_array = my_array_split[2]
#        cv2.erode(my_array, my_array, iterations=1)
#        cv2.dilate(my_array, my_array, iterations=1)
    
#        print "nbre de ligne ",(my_array2.shape[0])
        my_array2 = my_array * np.logical_and(my_array >= 0,my_array <= 1000)

        a=0
        if long_test == 0:
            img_moy = my_array2
            print "long test 0000000000000000"
        else :
            print img_moy.shape[0]
            print "long test 111111111111111111"
            img_moy = np.add (img_moy, my_array2) 
            img_moy/=2
    img_moy = img_moy.astype(np.uint8)
    cv2.imshow("img_moy", img_moy.astype(np.uint8))


    print img_moy.shape[0]
    print "long test 22222222"
    for i in range (0 ,img_moy.shape[0] , 1) :
        print i, img_moy.shape[0] , np.mean(img_moy[i,:])
        if ( np.mean(img_moy[i,:]) >= 100 ):
            print "long test 333333333333"

#            print "ligne ",i,int(np.mean(my_array2[i,:]))
            if a==0:
                    my_thresholdarray  = np.array ([ [i , int(np.mean(img_moy[i,:]))] ])
                    a+=1
            else :
                my_thresholdarray = np.append(my_thresholdarray, [ [i,int(np.mean(img_moy[i,:])) +10 ] ] , axis =0)
    print"themy_thresholdarray",   my_thresholdarray , my_thresholdarray.shape, my_thresholdarray.shape[0]
    
#    for i in range (my_thresholdarray)
    
make_my_thresholdarray()

while 1:
    get_depth0()
    #cv.ShowImage('Video1', get_depth1())
    if cv.WaitKey(10) == 27:
        break
#    break

