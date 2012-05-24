# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 12:00:13 2012

@author: tropic
"""

import numpy as np
import threading
import time
import socket

class VP:
    def __init__(self, vps):
        self.vps = vps
        self.server_IP="10.42.0.101"
        self.server_PORT=7005
        self.client_PORT=7006

        
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
            return np.fromstring(Donnee, dtype='f')


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
            print"data =" ,Donnee , Client
            #Donnee = ( x + y + z +";")*nbr_player)
            datasplit = Donnee.split(";")
    #	print "datasplit =" , datasplit
            if (Client[0] == "10.42.0.1"): # test par pure data
                print "datasplit =" , datasplit
                #datasplit1 = datasplit[0].split(";")

                store_blob = [[float(each2) for each2 in each.split(" ") ] for each in datasplit[:len(datasplit)-1]]
#                print "store =" ,store_blob 
                #store_blob=store_blob[0] 
                print "store =" ,store_blob 


                #para_data = store_blob[0][3:]
#                print "the paradata are",para_data

            else:
                store_blob = [[float(each2) for each2 in each.split(",") ] for each in datasplit]
                #store_blob[0][1] /= 100

            
#            if (positions!=None) : 
#                print "the pos are ", positions
#                for position in positions:
#                    print 'pos de 0' , position[0]
#                    position[0] /= 100
#                    position[1] /= 100
#                    position[2] /= 100
#                #positions.append(positions)
#                print"the good are ",   positions
            store_blob = [ [float(k)/100. for k in position] for position in store_blob ]
    #	store_blob = [ int(each2) for each2 in datasplit[0].split(" ") ]
            return store_blob

    def trigger(self):
        self.send_sock.sendto("1", (self.kinects['send_UDP_IP'], self.kinects['send_UDP_PORT']) )
        
        

class Affiche2(threading.Thread):
    def __init__(self, nom = ''):
        threading.Thread.__init__(self)
        self.nom = nom
        self._stopevent = threading.Event( )
        self.server_IP="10.42.0.1"
        self.server_PORT=7005
        
        #----VP.Server
        self.server_receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM ) # UDP
        self.server_receiver.bind(("", self.server_PORT))
        self.server_receiver.setblocking(0)
        self.server_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM ) # UDP
        
    def run(self):
        i = 0
        while not self._stopevent.isSet():
            try :
                Donnee, Client = self.server_receiver.recvfrom (512)
            except (KeyboardInterrupt):
                raise
            except:
                pass # detect = 0
            else :
#                print "ok", Client [0]
                str_send = particles[0:6, :].tostring('F')
                self.server_send.sendto(str_send, (Client[0], self.client_PORT) ) 
        print "le thread "+self.nom +" s'est termine proprement"
    def stop(self):
        self._stopevent.set( )
        