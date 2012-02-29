# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 15:58:46 2012

@author: laurent
"""
import numpy as np
import time
t = time.time()


#HACK
#N_Y, N_Z = 1240, 1024
N_Y, N_Z = 960, 600 # enigma
# Projection information
# ----------------------
f_async = 0. # if we do an asynchronnous masking of particles set it to some percentage > 0. / full sparseness with 1.
# taille du plan de reference
d_y, d_z = 4.54, 4.54*3/4#N_Z/N_Y # en metres
# distance du plan de reference
d_x = 8.5 # en metres
# position spatiale des VPs par rapport au centre du plan de reference
x_VPs = [d_x, d_x, d_x ] # en metres; placement regulier en profondeur a equidistance du plan de ref (le long d'un mur)
y_VPs = [.9*d_y, .1*d_y, .5*d_y ] # en metres; placement regulier, le centre en premier
z_VPs = [d_z/2, d_z/2, d_z/2] # en metres; on a place les VPs a la hauteur du centre du plan de reference

class Scenario(object):
    def __init__(self, N, scenario='calibration', center=np.array([d_x, d_y/2, d_z/2])):
        self.N = N
        self.particles = np.zeros((6, N), dtype=np.float32)
        # x, l’axe long, y l’axe transversal, z la hauteur
#        self.particles[0, :] = np.random.rand(N) * d_x
#        self.particles[1, :] = np.random.rand(N) * d_y
#        self.particles[2, :] = np.random.rand(N) * d_z
#        self.particles[3:, :] = np.random.randn(3, N) * .01 # speed is measured in screen size per second
        #self.particles[2,:] = self.particles[1,:]
        #self.particles[3,:] = -self.particles[0,:]
        self.t = time.time()
        self.scenario = scenario
        self.center = center
        
    def do_scenario(self):
        self.t_last = self.t
        self.t = time.time()
        if self.scenario == 'calibration':
            self.particles = np.zeros((6, self.N), dtype=np.float32)
            self.particles[0, :], self.particles[1, :], self.particles[2, :] = 0., d_y/2, d_z/2 # central fixation dot
            frequency_rot, frequency_plane = .1, .05 # how fast the whole disk moves in Hz
            radius = .3 * d_z
            N_dots = 16
            angle = 2 * np.pi * frequency_plane * self.t + np.linspace(0, 2 * np.pi, N_dots)
            # a circle on the reference plane
            self.particles[0, :N_dots] = 0. # on the refrerence plane
            self.particles[1, :N_dots] = d_y/2 + radius * np.sin(angle)
            self.particles[2, :N_dots] = d_z/2 + radius * np.cos(angle)
            # a circle of same radius but in front going opposite sign
            self.particles[0, N_dots:2*N_dots] = 1. # on the reference plane
            self.particles[1, N_dots:2*N_dots] = d_y/2 + radius * np.sin(-angle)
            self.particles[2, N_dots:2*N_dots] = d_z/2 + radius * np.cos(-angle)
        elif self.scenario == 'calibration-grille':
            self.particles = np.zeros((6, self.N), dtype=np.float32)
            self.particles[0, :], self.particles[1,:], self.particles[2,:] = 0., d_y/2, d_z/2
            N_grille = 2 # nombre de lignes
            # lignes horizontales
            self.particles[0, :self.N/2] = 0. # on the reference plane
            self.particles[1, :self.N/2] = np.mod(np.linspace(0, d_y*N_grille, self.N/2), d_y)
            self.particles[2, :self.N/2] = np.floor(np.linspace(0, d_y*N_grille, self.N/2) / d_y)*d_z/N_grille
            # lignes verticales
            self.particles[0, self.N/2:] = 1. # on the reference plane
            self.particles[1, self.N/2:] = np.floor(np.linspace(0, d_z*N_grille, self.N/2) / d_z)*d_y/N_grille
            self.particles[2, self.N/2:] = np.mod(np.linspace(0, d_z*N_grille, self.N/2), d_z)
            self.particles[0, 0], self.particles[1,0], self.particles[2,0] = 0., d_y/2, d_z/2 # central fixation dot
            
        elif self.scenario == 'rotating-circle':
            self.particles = np.zeros((6, self.N), dtype=np.float32)
            self.particles[0, :], self.particles[1,:], self.particles[2,:] = 0., d_y/2, d_z/2
            frequency_rot, frequency_plane = .1, .05 # how fast the whole disk moves in Hz
            radius_min, radius_max = .25 * d_z, .4 * d_z
            N_dots = 16
            N_rot = self.N / N_dots
            angle = 2 * np.pi *  frequency_plane *  self.t + np.linspace(0, 2 * np.pi * N_rot, self.N, endpoint=False)
            radius = np.linspace(radius_min, radius_max, self.N)
    
            # a circle on a rotating plane
            self.particles[0, :] = d_x/4 + radius * np.sin(angle) * np.sin(2*np.pi*frequency_rot*self.t)
            self.particles[1, :] = d_y/2 + radius * np.sin(angle) * np.cos(2*np.pi*frequency_rot*self.t)
            self.particles[2, :] = d_z/2 + radius * np.cos(angle)
    
        elif self.scenario == 'flock':
            # règle basique d'évitement
            for i in range(self.N):
                distance_moy = np.sqrt((self.particles[0,:] - self.particles[0, i])**2 + (self.particles[1,:] - self.particles[0, i])**2).mean()
                self.particles[2:4, i] += np.random.randn(2) *.001 * distance_moy
        #        self.particles[2:4, i] *= np.exp(- distance / 5. )
        #
            # règle basique de clustering des vitesses de particules proches
            for i in range(self.N):
                distance = np.sqrt((self.particles[0,:] - self.particles[0, i])**2 + (self.particles[1,:] - self.particles[0, i])**2)
                weights = np.exp(- distance**2 /2 / .1**2 )
                weights /= weights.sum()
        #        self.particles[2:4, i] *= np.random.randn(2) *.001 * distance
        #        self.particles[2:4,:] *= .99
                self.particles[2:4, i] += .01 * (self.particles[2:4, i] - (self.particles[2:4, :] * weights).sum() )
    
#            self.particles[0:2, :] += (t - t_last ) *  self.particles[2:4,:]
            self.particles[2:4, :] += np.random.randn(2,self.N) *.0001
            self.particles[2:4, :] *= .99
    
    
    #    self.particles[0,:] = np.mod(self.particles[0,:], N_X)
    #    self.particles[1,:] = np.mod(self.particles[1,:], N_Y)
    
    
    # fonco utilisée en version BITMAP à virer quand on pasera en pure openGL        
    def projection(self, i_VP, channel=None, xc=0, yc=0., zc=0., f_async=f_async): # yc=d_y/2., zc=d_z/2.):#
        # (xc, yc, zc) = coordonnees en metres du point (a gauche, en bas) du plan de reference
    
        # TODO remove particles that are outside the depth range
    
        # convert the position of each particle to a el, az coordinate projected on the reference plane
        x, y, z = self.particles[0, :], self.particles[1, :], self.particles[2, :]
        az = ((yc-y)*(xc-x_VPs[i_VP])-(yc-y_VPs[i_VP])*(xc-x))/(x_VPs[i_VP]-x)
        el = ((zc-z)*(xc-x_VPs[i_VP])-(zc-z_VPs[i_VP])*(xc-x))/(x_VPs[i_VP]-x)
#        # remove those that are outside the VP range
#        az = az[0 < az < d_y]
#        el = el[0 < el < d_z]
        # convert to integers
        az, el = np.floor(az*N_Y/d_y), np.floor(el*N_Z/d_z)
        image = np.ones((N_Z, N_Y, 4), dtype=np.float32)
        async_do = np.arange(self.N)[np.random.rand(self.N) > f_async]
        #rgba = [0, 1, 2, 3]
        #if not(channel==None): rgba.remove(channel)
        for i in async_do:
            if (0 <  az[i] < N_Y) and (0 < el[i] < N_Z):
                image[el[i], az[i], 0] = 0.
    
        return image
