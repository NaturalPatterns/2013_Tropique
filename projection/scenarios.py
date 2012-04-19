# -*- coding: utf-8 -*-
"""
Scenarios


"""

import numpy as np
import time

class Scenario:
    def __init__(self, N, scenario, volume, VPs, p):
        self.t = time.time()
        self.scenario = scenario
        self.volume = volume
        d_x, d_y, d_z = self.volume
        self.center = np.array([d_x/2, d_y/2, d_z/2]) # central fixation dot on the reference plane
        self.roger = np.array([d_x/2, d_y/2, d_z/2]) #  fixation dot  (AKA Roger?)
        self.origin = np.array([0., 0., 0.]) # origin

        self.VPs = VPs
        self.p = p
        self.N = N
#        self.speed_0 = 0.1 # average speed in m/s

        self.order = 2
        self.particles = np.zeros((6*self.order, N)) # x, y, z, u, v, w
        self.particles[0:6, :] = np.random.randn(6, self.N)*d_y/16
        self.particles[0:3, :] += self.center[:, np.newaxis]
        self.particles[3:6, :] += self.center[:, np.newaxis]

    def champ(self, position):

        # HACK: on place tous les segments sur le plan du fond pour avoir une approximation de l'espace perceptuel
        self.particles[0, :] = self.center[0]
        self.particles[3, :] = self.center[0]
        self.particles[6, :] = 0.
        self.particles[9, :] = 0.
        
        force = np.zeros((6,self.N)) # one vector per point
        ##forces globales
        
        # TODO :  gravité vers le bas pour séparer 2 phases
        
        # TODO :  passer en coordonnées perceptuelles / utiliser la position des VPs 
        # todo : éviter plaquage le long de bords
        
        if not(position==None) and not(position==np.nan):
            position[0] = self.center[0]
#            position[1] += 1. 

            OA =  self.particles[0:3, :] - np.array(position)[:, np.newaxis]# 3 x N
            distance = np.sqrt(np.sum(OA**2, axis=0)) # en metres
            gravity = - OA * (distance - self.p['distance_m'])/(distance + self.p['eps'])**4 # en metres
#            gravity = - self.p['G_global'] *  (D_ij)/(distance + self.p['eps'])**3 # en metres
#            print gravity.shape, distance.shape, D_ij.shape
            force[0:3, :] += self.p['G_global'] * gravity
            OB = self.particles[3:6, :]-np.array(position)[:, np.newaxis]
            distance = np.sqrt(np.sum(OB**2, axis=0)) # en metres
            gravity = - OB * (distance - self.p['distance_m'])/(distance + self.p['eps'])**4 # en metres
#            gravity = - self.p['G_global'] *  (D_ij)/(distance + self.p['eps'])**3 # en metres
            force[3:6, :] += self.p['G_global'] * gravity
    
            AB = self.particles[3:6, :] - self.particles[0:3, :]# 3 x N
            OC = (self.particles[0:3, :]+self.particles[3:6, :])/2-np.array(position)[:, np.newaxis]
            sinAB_OC = (AB[1, :]*OC[2,:] - AB[2, :]*OC[1,:]) # 1 x N
            sinAB_OC /= np.sqrt(np.sum(AB[1:]**2, axis=0)) + self.p['eps']
            sinAB_OC /= np.sqrt(np.sum(OC[1:]**2, axis=0)) + self.p['eps']
#            print AB.shape, np.hstack((AB[1,:],-AB[0,:])).shape
            rotation =  sinAB_OC  * np.vstack((AB[0,:], -AB[2,:], AB[1,:])) / np.sqrt(np.sum(AB**2, axis=0))

            force[0:3, :] += self.p['G_rot'] * rotation
            force[3:6, :] -= self.p['G_rot'] * rotation
                

        ## forces entres les particules
        
        # attraction / repulsion des extremites des segments
        
        AB = self.particles[0:3, :, np.newaxis]-self.particles[0:3, np.newaxis, :]
        distance = np.sqrt(np.sum(AB**2, axis=0)) # en metres
        gravity = -.25 * self.p['G_centre'] *  np.sum(AB/(distance.T + self.p['eps'])**3, axis=1) # en metres
        force[0:3, :] += self.p['G_centre'] * gravity
        force[3:6, :] += self.p['G_centre'] * gravity
        AB = self.particles[3:6, :, np.newaxis]-self.particles[3:6, np.newaxis, :]
        distance = np.sqrt(np.sum(AB**2, axis=0)) # en metres
        gravity = -.25 * self.p['G_centre'] * np.sum(AB/(distance.T + self.p['eps'])**3, axis=1) # en metres
        force[0:3, :] += self.p['G_centre'] * gravity
        force[3:6, :] += self.p['G_centre'] * gravity
        AB = self.particles[0:3, :, np.newaxis]-self.particles[3:6, np.newaxis, :]
        distance = np.sqrt(np.sum(AB**2, axis=0)) # en metres
        gravity = -.5 * self.p['G_centre'] * np.sum(AB/(distance.T + self.p['eps'])**3, axis=1) # en metres
        force[0:3, :] += self.p['G_centre'] * gravity
        force[3:6, :] += self.p['G_centre'] * gravity

#            rot = np.hstack((AB[1,:],-AB[0,:]))

#        # attraction / repulsion des centres des segments
#        centres = (self.particles[0:3, :]+self.particles[3:6, :])/2
#        D_ij = centres[:, :, np.newaxis]-centres[:, np.newaxis, :] # 3 x N x N
#        distance = np.sqrt(np.sum(D_ij**2, axis=0)) # N; en metres
#        gravity = np.sum(D_ij/(distance.T + self.p['eps'])**3, axis=1)# 3 x N en metres
#        
#        force[0:3, :] += self.p['G_centre'] * gravity
#        force[3:6, :] += self.p['G_centre'] * gravity
        # ressort

        AB = self.particles[0:3, :]-self.particles[3:6, :] # 3 x N
        distance = np.sqrt(np.sum(AB**2, axis=0)) # en metres
#        print force.shape, (distance[np.newaxis, :] - l_seg).shape, D_ij.shape, self.particles[6:12, :].shape
        force[0:3, :] -= self.p['G_spring'] * (distance[np.newaxis, :] - self.p['l_seg']) * AB / (distance[np.newaxis, :] + self.p['eps']) 
        force[3:6, :] += self.p['G_spring'] * (distance[np.newaxis, :] - self.p['l_seg']) * AB / (distance[np.newaxis, :] + self.p['eps']) 
        
        # damping        
        # force -= self.p['damp'] * self.particles[6:12, :]

        # HACK: on place tous les segments sur le plan du fond pour avoir une approximation de l'espace perceptuel
        self.particles[0, :] = self.center[0]
        self.particles[3, :] = self.center[0]
        self.particles[6, :] = 0.
        self.particles[9, :] = 0.

        force *= self.p['speed_0'] 
        
        return force
            

    def do_scenario(self, position=None):
        self.t_last = self.t
        self.t = time.time()
        dt = (self.t - self.t_last)
        d_x, d_y, d_z = self.volume
        
        if self.scenario == 'calibration':
#             self.particles = np.zeros((6, self.N))

            longueur_segments, undershoot_z = .05, .5
            # ligne horizontale
            self.particles[0, :self.N/2] = self.center[0] # on the reference plane
            self.particles[1, :self.N/2] = np.linspace(0, d_y, self.N/2)
            self.particles[2, :self.N/2] = self.center[2] - longueur_segments/2 - undershoot_z
            self.particles[3, :self.N/2] = self.center[0] # on the reference plane
            self.particles[4, :self.N/2] = np.linspace(0, d_y, self.N/2)
            self.particles[5, :self.N/2] = self.center[2] + longueur_segments/2 - undershoot_z
            # ligne verticale
            self.particles[0, self.N/2:] = self.center[0] # on the reference plane
            self.particles[1, self.N/2:] = self.center[1] - longueur_segments/2
            self.particles[2, self.N/2:] = np.linspace(0, d_z, self.N/2)
            self.particles[3, self.N/2:] = self.center[0] # on the reference plane
            self.particles[4, self.N/2:] = self.center[1] + longueur_segments/2
            self.particles[5, self.N/2:] = np.linspace(0, d_z, self.N/2)
            
#            print self.particles.mean(axis=1)

        elif self.scenario == 'fan':
#             self.particles = np.zeros((6, self.N))
            frequency_rot, frequency_plane = .1, .005 # how fast the whole disk moves in Hz
            radius_min, radius_max = 2.0, 5.0
            radius, length_ratio = .2 * d_z, 1.4
            N_dots = np.min(16, self.N)
            
#            N_dots = 50
#            radius, length_ratio = .1 * d_z, 2
            angle = 2 * np.pi * frequency_plane * self.t + np.linspace(0, 2 * np.pi, N_dots)

            # a circle drawn on a rotating plane
            self.particles[0, :N_dots] = self.center[0] #+ radius #* np.sin(angle) #* np.sin(2*np.pi*frequency_rot*self.t)
            self.particles[1, :N_dots] = self.center[1] + radius * np.sin(angle) #* np.cos(2*np.pi*frequency_rot*self.t)
            self.particles[2, :N_dots] = self.center[2] + radius * np.cos(angle)
            self.particles[3, :N_dots] = self.center[0] #+ radius * length_ratio  #* np.sin(angle) #* np.sin(2*np.pi*frequency_rot*self.t)
            self.particles[4, :N_dots] = self.center[1] + radius * length_ratio  * np.sin(angle) #* np.cos(2*np.pi*frequency_rot*self.t)
            self.particles[5, :N_dots] = self.center[2] + radius * length_ratio  * np.cos(angle)
#            self.particles[0:3, N_dots:] = self.origin[:, np.newaxis] # un rayon vers l'origine
#            self.particles[3:6, N_dots:] = self.origin[:, np.newaxis] + .0001 # très fin
                        
        elif self.scenario == '2fan':
#             self.particles = np.zeros((6, self.N))
            frequency_rot, frequency_plane = .1, .05 # how fast the whole disk moves in Hz
            radius, length_ratio = .2 * d_z, 1.4
            N_dots = np.min(16, self.N)
            angle = 2 * np.pi * frequency_plane * self.t + np.linspace(0, 2 * np.pi, N_dots)
            # a circle on the reference plane
            self.particles[0, :N_dots] = self.center[0] # on the refrerence plane
            self.particles[1, :N_dots] = self.center[1] + radius * np.sin(angle)
            self.particles[2, :N_dots] = self.center[2] + radius * np.cos(angle)
            self.particles[3, :N_dots] = self.center[0] # on the refrerence plane
            self.particles[4, :N_dots] = self.center[1] + radius * length_ratio * np.sin(angle)
            self.particles[5, :N_dots] = self.center[2] + radius * length_ratio * np.cos(angle)
            # a circle of same radius but in front going opposite sign
            self.particles[0, N_dots:2*N_dots] = self.center[0] + 1. # on the reference plane
            self.particles[1, N_dots:2*N_dots] = self.center[1] + radius * np.sin(-angle)
            self.particles[2, N_dots:2*N_dots] = self.center[2] + radius * np.cos(-angle)
            self.particles[3, N_dots:2*N_dots] = self.center[0] + 1. # on the reference plane
            self.particles[4, N_dots:2*N_dots] = self.center[1] + radius * length_ratio * np.sin(-angle)
            self.particles[5, N_dots:2*N_dots] = self.center[2] + radius * length_ratio * np.cos(-angle)
            self.particles[0:3, 2*N_dots:] = self.origin[:, np.newaxis] # un rayon vers l'origine
            self.particles[3:6, 2*N_dots:] = self.origin[:, np.newaxis] + .001 # très fin
            
        elif self.scenario == 'rotating-circle':
#             self.particles = np.zeros((6, self.N))
            frequency_rot, frequency_plane = .1, .05 # how fast the whole disk moves in Hz
            N_dots = np.min(16, self.N)
            radius, length_ratio = .3 * d_z, 2.5
            angle = 2 * np.pi * frequency_plane * self.t + np.linspace(0, 2 * np.pi, N_dots)

            # a circle drawn on a rotating plane
            self.particles[0, :N_dots] = self.center[0] + radius * np.sin(angle) * np.sin(2*np.pi*frequency_rot*self.t)
            self.particles[1, :N_dots] = self.center[1] + radius * np.sin(angle) * np.cos(2*np.pi*frequency_rot*self.t)
            self.particles[2, :N_dots] = self.center[2] + radius * np.cos(angle)
            self.particles[3, :N_dots] = self.center[0] + radius * length_ratio  * np.sin(angle) * np.sin(2*np.pi*frequency_rot*self.t)
            self.particles[4, :N_dots] = self.center[1] + radius * length_ratio  * np.sin(angle) * np.cos(2*np.pi*frequency_rot*self.t)
            self.particles[5, :N_dots] = self.center[2] + radius * length_ratio  * np.cos(angle)
            self.particles[0:3, N_dots:] = self.origin[:, np.newaxis] # un rayon vers l'origine
            self.particles[3:6, N_dots:] = self.origin[:, np.newaxis] + .0001 # très fin

        elif self.scenario == 'leapfrog':
            self.particles[0:6, :] += self.particles[6:12, :] * dt/2
            force = self.champ(position=position)
            self.particles[6:12, :] += force * dt
            # application de l'acceleration calculée sur les positions
            self.particles[0:6, :] += self.particles[6:12, :] * dt/2


        elif self.scenario == 'euler':            
            force = self.champ(position=position)
            self.particles[6:12, :] += force * dt
            # application de l'acceleration calculée sur les positions
            self.particles[0:6, :] += self.particles[6:12, :] * dt

            
        if not(position==None) and not(position==np.nan) and not(self.scenario == 'euler') and not(self.scenario == 'leapfrog'):
#            print('je dois pas passer par là')
            self.particles[0:3, :] += np.array(position)[:, np.newaxis]
            self.particles[3:6, :] += np.array(position)[:, np.newaxis]
            self.particles[0:3, :] -= self.center[:, np.newaxis]
            self.particles[3:6, :] -= self.center[:, np.newaxis]

        #  permet de ne pas sortir du volume (todo: créer un champ répulsif aux murs...)
        for i in range(6): 
            self.particles[i, (self.particles[i, :] > self.volume[i%3]) ] = self.volume[i%3]
            self.particles[i, (self.particles[i, :] < 0.) ] = 0.


        # TODO : fonction tabou dans les scenarios: zone d'évitement des bords: passer en coordonnées perceptuelles / utiliser la position des VPs / utiliser la position des VPs 


if __name__ == "__main__":
    import line
    line.___doc___
