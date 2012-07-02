# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 12:00:13 2012
lib for networks , server ,client in tropic
@author: BIOGENE&lolo

"""
import numpy as np
import socket

class VP:
    def __init__(self, server_IP , server_PORT ,client_PORT ):
#        self.vps = vps
#        self.server_IP="10.42.0.101"
#        self.server_PORT=7005
#        self.client_PORT=7006
#        self.vps = vps
        self.server_IP = server_IP
        self.server_PORT = server_PORT
        self.client_PORT = client_PORT

        
        #----VP.Trigger
        self.client_send = socket.socket( socket.AF_INET, socket.SOCK_DGRAM ) # UDP
        #----VP.Server
        self.server_receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM ) # UDP
        self.server_receiver.bind(("", self.server_PORT))
        self.server_receiver.setblocking(0)

        self.server_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM ) # UDP
        #----Vp Client
        self.client_receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM ) # UDP
        self.client_receiver.bind( ("", self.client_PORT) )
        self.client_receiver.setblocking(0)
    
    #-----def VP.Trigger
    def trigger(self):
        self.client_send.sendto("1", (self.server_IP, self.server_PORT) )
    #-----def VP.Server
    def server(self, particles):
        try :
            Donnee, Client = self.server_receiver.recvfrom (8192)
        except (KeyboardInterrupt):
            raise
        except:
            pass # detect = 0
        else :
#            print "ok", Client [0]
#            str_send = particles[0:6, :].tostring('F')
#            self.server_send.sendto(str_send, (Client[0], self.client_PORT) ) 
            self.server_send.sendto(particles, (Client[0], self.client_PORT) ) 

    #-----def  VP.Listen
    def listen(self):
        try :
            Donnee, Client = self.client_receiver.recvfrom (8192)
        except (KeyboardInterrupt):
            raise
        except:
            pass # detect = 0
        else :
            #print"data =" , len(Donnee) , Client
#            return np.fromstring(Donnee, dtype='f')
            return Donnee



class Kinects:
    def __init__(self, kinects):
        self.kinects = kinects
        import socket

        print "UDP my port:", kinects['UDP_PORT']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM ) # UDP
        self.sock.bind((kinects['UDP_IP'], kinects['UDP_PORT']) )
        #sock.settimeout(0)
        self.sock.setblocking(0)

        print "UDP target IP:", kinects['send_UDP_IP']
        print "UDP target port:", kinects['send_UDP_PORT']
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM ) # UDP

    def read_sock(self):
        try :
            Donnee, Client = self.sock.recvfrom (128)
        except (KeyboardInterrupt):
            raise
        except:
           pass # detect = 0
        else :
#            print"data =" ,Donnee , Client
            #Donnee = ( x + y + z +";")*nbr_player)
            datasplit = Donnee.split(";")
    #	print "datasplit =" , datasplit
            if (Client[0] == "10.42.0.200"): # test par pure data
#                print "datasplit =" , datasplit
                store_blob = [[float(each2) for each2 in each.split(" ") ] for each in datasplit[:len(datasplit)-1]]
#                print "store =" ,store_blob 
            else:
                store_blob = [[float(each2) for each2 in each.split(",") ] for each in datasplit]

            store_blob = [ [float(k)/100. for k in position] for position in store_blob ]
            return store_blob

    def trigger(self):
        self.send_sock.sendto("1", (self.kinects['send_UDP_IP'], self.kinects['send_UDP_PORT']) )

        