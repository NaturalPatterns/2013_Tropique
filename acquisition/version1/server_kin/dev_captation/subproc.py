#!/usr/bin/env python
import subprocess
import socket
import time
import os
import signal
import fcntl
import struct

#global pipe
global pid
#print "mon pid = rien "

from parametres import info_kinects, DEBUG

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
    
my_ip = get_ip_address('eth0')
#print "my ip is =", my_ip
global nbr_process
nbr_process=0
for last in info_kinects:
    if last['address'] == my_ip:
        nbr_process +=1
#print "nbrof kinect =", nbr_process


#hom = subprocess.call("ps a | grep tropic_res", shell=True)
global DEBUG
global dis_shell
dis_shell = False

UDP_IP=""
UDP_PORT=3002
sock = socket.socket( socket.AF_INET, # Internet
                      socket.SOCK_DGRAM ) # UDP
sock.bind( (UDP_IP,UDP_PORT) )
sock.settimeout(1)

def open_capture():
    global pipe1 , pipe2, nbr_process
    global pid
    if nbr_process == 1 :
        my_str = "./server_kin_0.py"
        pipe1 = subprocess.Popen(my_str, shell=dis_shell)       
        if DEBUG : print "start server_kin_0.py  , pid = ", pipe1
   
    else :
        my_str = "./server_kin_0.py"
        pipe1 = subprocess.Popen(my_str, shell=dis_shell)
        my_str = "./server_kin_1.py"
        pipe2 = subprocess.Popen(my_str, shell=dis_shell)
        #pipe = subprocess.Popen(tropic_res.py,stdout=subprocess.PIPE,      stderr=subprocess.PIPE, shell=True)
        if DEBUG : print "start server_kin_0/1.py  , pid = ", pipe1, pipe2

def close_capture():
    global pipe1 , pipe2, nbr_process
    if nbr_process == 1 :    
        ju1  = pipe1.terminate()
        pi1 = pipe1.kill()
        pipe1.send_signal(signal.SIGKILL)
        if DEBUG : print "cest finiiiiiiiiii pour pipe ",pipe1
    else :
        if DEBUG : print "cest finiiiiiiiiii pour pipe ",pipe1, pipe2
        #rt = subprocess.Popen.terminate(pipe)
        ju1  = pipe1.terminate()
        pi1 = pipe1.kill()
        pipe1.send_signal(signal.SIGKILL)
        ju2  = pipe2.terminate()
        pi2 = pipe2.kill()
        pipe2.send_signal(signal.SIGKILL)

def display():
    global pipe1 , pipe2, nbr_process
    global pid
    if nbr_process == 1 :
        my_str = "./server_kin_0_display.py"
        pipe1 = subprocess.Popen(my_str, shell=dis_shell)       
        if DEBUG : print "start server_kin_0_display.py  , pid = ", pipe1
   
    else :
        my_str = "./server_kin_0_display.py"
        pipe1 = subprocess.Popen(my_str, shell=dis_shell)
        my_str = "./server_kin_1_display.py"
        pipe2 = subprocess.Popen(my_str, shell=dis_shell)
        #pipe = subprocess.Popen(tropic_res.py,stdout=subprocess.PIPE,      stderr=subprocess.PIPE, shell=True)
        if DEBUG : print "start server_kin_0/1_display.py  , pid = ", pipe1, pipe2

while 1:
    try:
        data, addr = sock.recvfrom( 1024 )
    except socket.error, msg:
        rien = 0
    else:
        my_com = int(data)
        if DEBUG : print "com" , my_com
        if my_com == 1:
            open_capture()
        if my_com == 0:
            close_capture()
        if my_com == 2:
            display()

		

