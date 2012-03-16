# -*- coding: utf-8 -*-
"""
Scenarios


"""
import numpy as np
import time
t = time.time()

class Scenario(object):
    def __init__(self, N, scenario, VPs):
        self.t = time.time()
        self.scenario = scenario
        self.center = np.array([d_x, d_y/2, d_z/2])
        self.VPs = VPs
        self.volume = volume
        self.N = N
        self.speed_0 = 0.1 # average speed in m/s
        self.particles = np.zeros((6, N), dtype=np.float32) # x, y, z, u, v, w
        d_x, d_y, d_z = self.volume
        self.particles[0, :], self.particles[1,:], self.particles[2,:] = 0., np.random.randn(self.N)*d_y/16+d_y/2, np.random.randn(self.N)*d_y/16 + d_z/2
#        self.particles[0, :], self.particles[1,:], self.particles[2,:] = 0., np.random.rand(self.N)*d_y, np.random.randn(self.N)*d_z
        self.particles[3:6, :] = np.random.randn(3, self.N)*self.speed_0
        # x, l’axe long, y l’axe transversal, z la hauteur
#        self.particles[0, :] = np.random.rand(N) * d_x
#        self.particles[1, :] = np.random.rand(N) * d_y
#        self.particles[2, :] = np.random.rand(N) * d_z
#        self.particles[3:, :] = np.random.randn(3, N) * .01 # speed is measured in screen size per second
        #self.particles[2,:] = self.particles[1,:]
        #self.particles[3,:] = -self.particles[0,:]

    def do_scenario(self):
         self.t_last = self.t
         self.t = time.time()
         d_x, d_y, d_z = self.volume
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

        elif self.scenario == 'gray-scott':
            sigma, distance_m = .5, .2 # how fast the whole disk moves in Hz
            diff, diff_noise = .02, 0.005 # diffusion speed

            y, z = self.particles[1, :], self.particles[2,:]
            Dy, Dz = np.mod(y[:, np.newaxis]-y.T + d_y/2., d_y) - d_y/2., np.mod(z[:, np.newaxis]-z.T + d_z/2., d_z) - d_z/2.
            distance = np.sqrt(Dy**2 + Dz**2) # en metres
#            print distance, distance.mean()
            speed = (distance-distance_m)*(np.exp(-(distance-distance_m)**2/2/sigma**2))
#            speed = (distance-distance_m)*(np.exp(-np.abs(distance-distance_m)/sigma))
            speed /= np.sqrt(speed**2).mean() 
            speed *= self.speed_0
#            print speed.mean()*(self.t - self.t_last), (self.t - self.t_last)
#            print y.mean(), z.mean(), y.std(), z.std()
            dt =  (self.t - self.t_last)
            self.particles[0, :] = 0. # on the refrerence plane
            
            speed_y = (Dy * speed).mean(axis=1)
            speed_z = (Dz * speed).mean(axis=1)

            self.particles[4, :] += diff * (speed_y - self.particles[4, :])
            self.particles[5, :] += diff * (speed_z - self.particles[5, :])

            self.particles[4, :] += diff_noise * np.random.randn(self.N)
            self.particles[5, :] += diff_noise * np.random.randn(self.N)
            
            self.particles[1, :] += self.particles[4, :] * dt
            self.particles[2, :] += self.particles[5, :] * dt

            self.particles[1, :] = np.mod(self.particles[1, :], d_y)
            self.particles[2, :] = np.mod(self.particles[2, :], d_z)
        
    
    # fonction utilisée en version BITMAP à virer quand on pasera en pure openGL        
#    def projection(self, i_VP, channel=None, xc=0, yc=0., zc=0., f_async=f_async, N_Y=N_Y, N_Z=N_Z): # yc=d_y/2., zc=d_z/2.):#
        # (xc, yc, zc) = coordonnees en metres du point (a gauche, en bas) du plan de reference
    
        # TODO remove particles that are outside the depth range
#    
#        # convert the position of each particle to a el, az coordinate projected on the reference plane
#        x, y, z = self.particles[0, :], self.particles[1, :], self.particles[2, :]
#        az = ((yc-y)*(xc-x_VPs[i_VP])-(yc-y_VPs[i_VP])*(xc-x))/(x_VPs[i_VP]-x)
#        el = ((zc-z)*(xc-x_VPs[i_VP])-(zc-z_VPs[i_VP])*(xc-x))/(x_VPs[i_VP]-x)
##        # remove those that are outside the VP range
##        az = az[0 < az < d_y]
##        el = el[0 < el < d_z]
#        # convert to integers
#        az, el = np.floor(az*N_Y/d_y), np.floor(el*N_Z/d_z)
#        
#        
##        async_do = np.arange(self.N)[np.random.rand(self.N) > f_async]
#        #rgba = [0, 1, 2, 3]
#        #if not(channel==None): rgba.remove(channel)
#        image = np.ones((N_Z, N_Y, 4), dtype=np.float32)
#        for i in xrange(self.N): #async_do:
#            if (0 <  az[i] < N_Y) and (0 < el[i] < N_Z):
#                image[el[i], az[i], 0] = 0.    
#        #return image
#        return self.particles[0:3, :]
