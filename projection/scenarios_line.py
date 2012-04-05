# -*- coding: utf-8 -*-
"""
Scenarios


"""

import numpy as np
import time

class Scenario:
    def __init__(self, N, scenario, volume, VPs):
        self.t = time.time()
        self.scenario = scenario
        self.volume = volume
        d_x, d_y, d_z = self.volume
        self.center = np.array([5.5, d_y/2, d_z/2]) # central fixation dot on the reference plane
        self.roger = np.array([d_x/2, d_y/2, d_z/2]) #  fixation dot 
        self.origin = np.array([0., 0., 0.]) # central fixation dot (AKA Roger?)

        self.VPs = VPs
        self.N = N
        self.speed_0 = 0.1 # average speed in m/s

        self.order = 2
        self.particles = np.zeros((6*self.order, N)) # x, y, z, u, v, w
        self.particles[0:6, :] = np.random.randn(6, self.N)*d_y/16
        self.particles[0:3, :] += self.center[:, np.newaxis]
        self.particles[3:6, :] += self.center[:, np.newaxis]
#        if self.scenario == 'champ':
            

    def do_scenario(self, position=None):
        self.t_last = self.t
        self.t = time.time()
        dt = (self.t - self.t_last)
        d_x, d_y, d_z = self.volume
        
        if self.scenario == 'calibration-grille':
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
            
            print self.particles.mean(axis=1)
            
        elif self.scenario == 'calibration':
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
            radius_min, radius_max = .25 * d_z, .4 * d_z
            N_dots = 16
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


        elif self.scenario == 'champ':
            # NOTE: on va déjà se placer dans le cas simple où l'observateur (Roger) est fixe, au centre
            sigma, distance_m = .1, 0.4
            G_end, G_spring, G_centre, eps = 1.e-5, 1.e-4, 1.e-4, 1.e-3

            # HACK: on place tous les segments sur le plan du fond pour avoir une parrocximation de l'espace perceptuel
            self.particles[0, :] = self.center[0]
            self.particles[3, :] = self.center[0]

            self.particles[0:6, :] += self.particles[6:12, :] * dt/2
            
            # attraction / repulsion des extremites des segments
            D_ij = self.particles[0:3, :, np.newaxis]-self.particles[0:3, np.newaxis, :]
            distance = np.sqrt(np.sum(D_ij**2, axis=0)) # en metres
            force = np.sum(D_ij/(distance.T + eps)**3, axis=1)#self.N # en metres
            D_ij = self.particles[3:6, :, np.newaxis]-self.particles[3:6, np.newaxis, :]
            distance = np.sqrt(np.sum(D_ij**2, axis=0)) # en metres
            force += np.sum(D_ij/(distance.T + eps)**3, axis=1)#self.N # en metres
            self.particles[6:9, :] += G_end * force * dt
            self.particles[9:12, :] += G_end * force * dt
#
#            # attraction / repulsion des centres des segments
#            centres = (self.particles[0:3, :]+self.particles[3:6, :])/2
#            D_ij = centres[:, :, np.newaxis]-centres[:, np.newaxis, :]
#            distance = np.sqrt(np.sum(D_ij**2, axis=0)) # en metres
#            force = np.sum(D_ij/(distance.T + eps)**3, axis=1)#/self.N # en metres
#            
#            self.particles[6:9, :] += G_centre * force * dt
#            self.particles[9:12, :] += G_centre * force * dt
            
            # ressort
            G, eps = 1.e-4, 1e-3
            l_seg = 1.2
            D_ij = self.particles[0:3, :]-self.particles[3:6, :]
            distance = np.sqrt(np.sum(D_ij**2, axis=0)) # en metres
            print distance[np.newaxis, :].shape, D_ij.shape, self.particles[6:12, :].shape
            force = np.sum(D_ij*((distance[np.newaxis, :] - l_seg)/(distance[np.newaxis, :] + eps)**1), axis=1)/self.N # en metres
            self.particles[6:9, :] += G_spring * force * dt
            self.particles[9:12, :] += G_spring * force * dt

            # application de l'acceleration calculée sur les positions
            self.particles[0:6, :] += self.particles[6:12, :] * dt/2

            for i in range(6): 
                self.particles[i, [self.particles[i, :] > self.volume[i%3]] ] = self.volume[i%3]
                self.particles[i, [self.particles[i, :] < 0.] ] = 0.
#                
#            self.particles[0, :] = np.mod(self.particles[0, :], d_x)
#            self.particles[1, :] = np.mod(self.particles[1, :], d_y)
#            self.particles[2, :] = np.mod(self.particles[2, :], d_z)
#            self.particles[3, :] = np.mod(self.particles[3, :], d_x)
#            self.particles[4, :] = np.mod(self.particles[4, :], d_y)
#            self.particles[5, :] = np.mod(self.particles[5, :], d_z)
            
        if not(position==None) and not(position==np.nan):
            self.particles[0:3, :] += np.array(position)[:, np.newaxis]
            self.particles[3:6, :] += np.array(position)[:, np.newaxis]
            self.particles[0:3, :] -= self.center[:, np.newaxis]
            self.particles[3:6, :] -= self.center[:, np.newaxis]

if __name__ == "__main__":
    import line