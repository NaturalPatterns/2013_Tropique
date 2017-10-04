#!/usr/bin/env python
# -*- coding: utf8 -*-
import freenect
import cv2
import cv
import numpy as np
import socket
import sys
import fcntl
import struct
global my_thresholdarray
import os

sys.path.append('..')
from parametres_vasarely import info_kinects

#-----parametre de normalisation des infos (pixel to metre)
global fx_d, fy_d, cx_d, cy_d
fx_d = 1.0 / 594.0
fy_d = 1.0 / 591.0
cx_d = 340
cy_d = 240

#------declaration de l'addresse et du numero de kinect utilisé dans send data
#print sys.argv[0], sys.argv[1], sys.argv[2] # nom du fichier, param1 , param2
global server_kin
server_kin = int(sys.argv[1])
print type(server_kin)
global show
show = (sys.argv[2] == "1")
print('Press ESC in window to stop')


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
my_ip = get_ip_address('eth0')
#my_ip = get_ip_address('wlan0')
#print "my ip is =", my_ip
global my_number
my_number = (int(my_ip[len(my_ip) - 2] + my_ip[len(my_ip) - 1]))
string_name = str(my_ip) + "," + str(my_number)
print my_ip, my_number, server_kin

#------declaration des fenetre d'afichage
print('Press ESC in window to stop')
if show:
    cv2.namedWindow(string_name, cv.CV_WINDOW_NORMAL)
    cv2.cv.MoveWindow(string_name, 1 + server_kin*400, 600)
    cv2.cv.ResizeWindow(string_name, 400, 400)
    cv2.namedWindow("0", cv.CV_WINDOW_NORMAL)
    cv2.cv.MoveWindow("0", 1 + server_kin*400, 100)
    cv2.cv.ResizeWindow("0", 400, 400)
#    cv2.namedWindow("img_moy",cv.CV_WINDOW_NORMAL)
#    cv2.cv.MoveWindow("img_moy",1 + server_kin*400,300)
#    cv2.cv.ResizeWindow("img_moy",400,400)
    
#---- definition du threshold (distance ) max etablie dans parametres.py
global threshold
threshold = 600
level = 5
#----creation de la socket UDP pour ecouter et repondre au serveur
#sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP
PySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
PySocket.bind(('', 9998 + server_kin))
PySocket.settimeout(0)

global good_z
global img_moy
img_moy = np.zeros((480, 640), np.uint8)

#----update valeur du threshold depuis le slider
def change_threshold(value):
    global threshold
#    print int( ((1.0/(float(value)/100))-3.33) / -0.003071)
    threshold = value
#----boucle de base ----------------------------------------------------------
def get_depth0():
    global my_thresholdarray
    global threshold
    global current_depth
    valu_array = [0, 0, 0, 0, 0, 0]
#    if os.path.exists("/dev/video0"):
#        print "video0 est la"
#    else:
#        print "la cest la mort"
    try:
        my_depth, timestamp = freenect.sync_get_depth(server_kin)
    except:
        print "la ya gros probleme"
    else:
        pass
    data = my_depth
    my_array = my_depth
    cv2.imshow("0", my_depth.astype(np.uint8))
    try:
        for nbr_test in range(0, my_thresholdarray.shape[0]):
#            my_array[my_thresholdarray[nbr_test][0]  ] = my_array[my_thresholdarray[nbr_test][0]] * np.less_equal( my_array[my_thresholdarray[nbr_test][0]],  my_thresholdarray[nbr_test][1])
            my_array[my_thresholdarray[nbr_test][0]] = my_array[my_thresholdarray[nbr_test][0]] * 0
    except:
#        print "echec floor substract"
        pass
#    my_array2 = 255 * np.logical_and(my_array >= current_depth - threshold,my_array <= current_depth + threshold)
    my_array2 = my_array * np.logical_and(my_array >= 0, my_array <= int(((1.0/(float(threshold)/100))-3.33) / -0.003071))
#    my_array2 = my_array * np.logical_and(my_array >= 0,my_array <= 2000)
#    print "threshold=",threshold , int( ((1.0/(float(threshold)/100))-3.33) / -0.003071)
#    cv2.imshow("1", my_array.astype(np.uint8))

    my_array2 = my_array2.astype(np.uint8)
    img2 = np.zeros((480, 640), np.uint8)
    img2 = my_array2
    h, w = img2.shape[:2]
    levels = 3
    contours0, hierarchy = cv2.findContours(img2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cv2.approxPolyDP(cnt, levels, True) for cnt in contours0]
#    send_string = str("")

    def update(levels):
        vis = np.zeros((h, w, 3), np.uint8)
        nbr = 0
        global send_string
        send_string = str("")
        global good_z
        for cnt in contours:
            if (len(cnt) > 8) and (cv2.contourArea(cnt) > 2000):
                centre = cv2.minAreaRect(cnt)
                a, x_moy, y_moy, x_max, y_max = 0, 0, 0, 0, 0
                x_min = 640
                y_min = 480
                for i in cnt:
                    #print "my i =",i
                    x = i[0][0]
                    y = i[0][1]
                    if (x > x_max):
                        x_max = x
                    if (x < x_min):
                        x_min = x
                    if (y > y_max):
                        y_max = y
                    if (y < y_min):
                        y_min = y
                    x_moy += x
                    y_moy += y
                    a += 1
                    #print "x , y = " ,x ,y
                    cv2.circle(vis, (x, y), 10, 255, 3)

                x_moy = int((x_min+x_max)/2)
                y_moy = int((y_min+y_max)/2)
                my_z = 0
                a = 0
                for i in(range(3)):
                    for k in (range(3)):
                        try:
                            if ((data[(y_moy - 1) + i][(x_moy - 1) + k]) <= 1024):
                                my_z += data[(y_moy-1)+i][(x_moy-1)+k]
                                a += 1
    #                                    print "good" , data [(y_moy-1)+i][(x_moy-1)+k]
                            else:
    #                                    print "the goodz is bad " , (data [(y_moy-1)+i][(x_moy-1)+k])
                                pass
                        except:
    #                                print "bad data"
                            pass
                global good_z
                if a!=0:
                    my_z = int(my_z / a)
                    good_z = my_z
#                    print "z , my_z = " , data [y_moy][x_moy], good_z
                    cv2.circle(vis, (x_moy, y_moy), 25, (255, 255), 3)
                    cv2.circle(vis, (int(centre[0][0]), (int(centre[0][1]))), 25, (255, 255, 255), 3)
                    cv2.circle(vis, (int((x_min + x_max) / 2), int((y_min + y_max) / 2)), 25, (0, 255, 255), 3)

                    valu_array[0] = my_number
                    valu_array[1] = server_kin
                    valu_array[2] = nbr
#                    valu_array[2]= x_moy
#                    valu_array[3]= y_min
                    depth = float(1.0 / (float(good_z) * -0.0030711016 + 3.3309495161))
                    valu_array[3] = int(float((x_moy - cx_d) * depth * fx_d)*100)
                    valu_array[4] = int(float((y_min - cy_d) * depth * fy_d)*100)
                    valu_array[5] = int(depth * 100)
                    nbr += 1
                    for val in valu_array:
                        send_string += str(val) + ","
#                    print send_string
                    send_string = send_string[0:(len(send_string) - 1)]
                    send_string += ";"
                else:
                    cv2.circle(vis, (x_moy, y_moy), 25, (0, 125, 255), 3)

#        levels = 5
        if show:
            cv2.drawContours(vis, contours, (-1, 3)[levels <= 0], (128, 255, 255), 3, cv2.CV_AA, hierarchy, abs(levels))
            vis = cv2.resize(vis, (320, 240))
            cv2.imshow(string_name, vis)
    update(levels)
    cv2.createTrackbar("depth", string_name, threshold, 1000, change_threshold)
#    print "sendstring",send_string
    try:
        Donnee, Client = PySocket.recvfrom(1024)
#        print "client is ", Client
    except:
        pass
    else:
        if Donnee == "data":
            PySocket.sendto(send_string, Client)
        if Donnee == "boot":
            os.system("reboot")
        if Donnee[:4] == "init":
            try:
                print "make_my_threshold", int(Donnee[5:])
                threshold = int(Donnee[5:])
            except:
                print "bad data to make_my_threshold"
            else:
                make_my_thresholdarray()


def make_my_thresholdarray():
    print "test  reduction bruit pour threshold = ", threshold
    global my_thresholdarray
#---- init kinect (1) pour rien)
    for long_test in range(10):
        the_depth, timestamp = freenect.sync_get_depth(server_kin)
#---- calcule image moyenne ( bruit moyen)
    img_moy = np.zeros((480, 640), np.uint8)
    for long_test in range(10):
        the_depth, timestamp = freenect.sync_get_depth(server_kin)
        data = the_depth
        global depth_hist, learn, record_list
        my_array = the_depth
        my_array2 = my_array * np.logical_and(my_array >= 0, my_array <= int( ((1.0/(float(threshold)/100))-3.33) / -0.003071))

        a = 0
        if long_test == 0:
            img_moy = my_array2
            print "test  reduction bruit 1"
        else:
#            print img_moy.shape[0]
#            print "test  reduction bruit 2"
            img_moy = np.add(img_moy, my_array2)
#        img_moy/=11
        img_moy = img_moy.astype(np.uint8)
#        if show :
#            cv2.imshow("img_moy", img_moy.astype(np.uint8))
    print img_moy.shape[0]
    print "test  reduction bruit 12"
    for i in range(0, img_moy.shape[0], 1):
#        print i, img_moy.shape[0] , np.mean(img_moy[i,:])
        if np.mean(img_moy[i, :]) >= 50:
#            print "test  reduction bruit 13"

#            print "ligne ",i,int(np.mean(my_array2[i,:]))
            if a == 0:
                    my_thresholdarray = np.array([[i, int(np.mean(img_moy[i, :]))]])
                    a += 1
            else:
                my_thresholdarray = np.append(my_thresholdarray, [[i, int(np.mean(img_moy[i, :])) + 10]], axis = 0)
    print "finish make_my_thresholdarray"

make_my_thresholdarray()

while 1:
    get_depth0()
    #cv.ShowImage('Video1', get_depth1())
    if cv.WaitKey(10) == 27:
        break
#    break
