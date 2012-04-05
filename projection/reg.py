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
        self.center = np.array([d_x/2, d_y/2, d_z/2])
        self.origin = np.array([0., 0., 0.]) # central fixation dot (AKA Roger?)
        self.VPs = VPs
        self.N = N
        self.speed_0 = 0.1 # average speed in m/s
        self.particles = np.zeros((6, N), dtype=np.float32) # x, y, z, u, v, w
        self.particles[0, :], self.particles[1,:], self.particles[2,:] = np.random.randn(self.N)*d_y/16, np.random.randn(self.N)*d_y/16+d_y/2, np.random.randn(self.N)*d_y/16 + d_z/2
        self.particles[3:6, :] = np.random.randn(3, self.N)*self.speed_0
        if self.scenario == 'N-body':
            self.particles[0:3, :] = np.random.randn(3, self.N)*d_y/32
            self.particles[0:3, :] += self.center[:, np.newaxis]
            self.particles[0:3, :(N/2)] += self.center[:, np.newaxis]/8
            self.particles[0:3, (N/2):] -= self.center[:, np.newaxis]/8

            self.speed_0 = 0.01 # average speed in m/s
            self.particles[3, :] = self.speed_0# (self.particles[2, :]-self.center[2])*self.speed_0
            self.particles[4, :] = -self.speed_0# (self.particles[1, :]+self.center[1])*self.speed_0
            self.particles[5, :] = 0 #np.random.randn(1, self.N)*self.speed_0

    def do_scenario(self, position=None):
        self.t_last = self.t
        self.t = time.time()
        dt = (self.t - self.t_last)
        d_x, d_y, d_z = self.volume
        if self.scenario == 'calibration':
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
            self.particles[0:3, 2*N_dots:] = self.origin[:, np.newaxis] # un point vers l'origine

        elif self.scenario == 'calibration-grille':
            self.particles = np.zeros((6, self.N), dtype=np.float32)

            # ligne horizontale
            self.particles[0, :self.N/2] = 0. # on the reference plane
            self.particles[1, :self.N/2] = np.linspace(0, d_y, self.N/2)
            self.particles[2, :self.N/2] = d_z/2
            # ligne verticale
            self.particles[0, self.N/2:] = 0. # on the reference plane
            self.particles[1, self.N/2:] = d_y/2
            self.particles[2, self.N/2:] = np.linspace(0, d_z, self.N/2)
            
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
            sigma, distance_m = .01, 0.4
            diff, diff_noise = .01, 0.001 # diffusion speed

            x, y, z = self.particles[0, :], self.particles[1, :], self.particles[2,:]
            Dx = np.mod(x[:, np.newaxis]-x.T + d_x/2., d_x) - d_x/2. # TODO: vectorize more!
            Dy = np.mod(y[:, np.newaxis]-y.T + d_y/2., d_y) - d_y/2.
            Dz = np.mod(z[:, np.newaxis]-z.T + d_z/2., d_z) - d_z/2.
            distance = np.sqrt(Dx**2 + Dy**2 + Dz**2) # en metres
#            print distance, distance.mean()
            speed = (distance-distance_m)*(np.exp(-(distance-distance_m)**2/2/sigma**2))

            # éviter le centre pour pas se cramer les yeux :-/
            distance = np.sqrt(y**2 + z**2) # en metres / cylindre dans l'axe de la salle / TODO: c'est pas terrible
            speed += np.exp(-distance**2/2/1.2**2)
#            speed = (distance-distance_m)*(np.exp(-np.abs(distance-distance_m)/sigma))
            speed /= np.sqrt(speed**2).mean()
            speed *= self.speed_0
#            print speed.mean()*(self.t - self.t_last), (self.t - self.t_last)
#            print y.mean(), z.mean(), y.std(), z.std()


            speed_x = (Dx * speed).mean(axis=1)
            speed_y = (Dy * speed).mean(axis=1)
            speed_z = (Dz * speed).mean(axis=1)

            self.particles[3, :] += diff * (speed_y - self.particles[3, :])
            self.particles[4, :] += diff * (speed_y - self.particles[4, :])
            self.particles[5, :] += diff * (speed_z - self.particles[5, :])

            self.particles[3, :] += diff_noise * np.random.randn(self.N)
            self.particles[4, :] += diff_noise * np.random.randn(self.N)
            self.particles[5, :] += diff_noise * np.random.randn(self.N)

            self.particles[0, :] += self.particles[3, :] * dt
            self.particles[1, :] += self.particles[4, :] * dt
            self.particles[2, :] += self.particles[5, :] * dt

            self.particles[0, :] = np.mod(self.particles[0, :], d_x)
            self.particles[1, :] = np.mod(self.particles[1, :], d_y)
            self.particles[2, :] = np.mod(self.particles[2, :], d_z)

        elif self.scenario == 'N-body':
            G = 1.e-10
#            D_ij = self.particles[0:3, :, np.newaxis]-self.particles[0:3, np.newaxis, :]
#            D_ij = np.mod(D_ij + self.volume/2., self.volume) - self.volume/2. # TODO: vectorize more!
#            print D_ij.shape
            
            Dx = np.mod(self.particles[0, :, np.newaxis]-self.particles[0, :].T + d_x/2., d_x) - d_x/2. # TODO: vectorize more!
            Dy = np.mod(self.particles[1, :, np.newaxis]-self.particles[1, :].T + d_y/2., d_y) - d_y/2.
            Dz = np.mod(self.particles[2, :, np.newaxis]-self.particles[2,:].T + d_z/2., d_z) - d_z/2.
            
            distance = np.sqrt(Dx**2 + Dy**2 + Dz**2) # en metres
            force = np.mean([Dx, Dy, Dz]/(distance.T +1e-6)**3, axis=1) # en metres
#            print Dx.shape, distance.shape, force.shape, np.mean(1/(distance+1e-6)**3, axis=1).shape
            # Euler            
            self.particles[3:6, :] += G * force * dt
            self.particles[0:3, :] += self.particles[3:6, :] *dt
#
#            # Midpoint method
#            self.particles[3:6, :] += G * force * dt
#            r = self.particles[0:3, :] + self.particles[3:6, :] * dt/2

            

            self.particles[0, :] = np.mod(self.particles[0, :], d_x)
            self.particles[1, :] = np.mod(self.particles[1, :], d_y)
            self.particles[2, :] = np.mod(self.particles[2, :], d_z)


        if not(position==None) and not(position==np.nan):
    #        self.particles[0, :] += position[0] - 5#- self.VPs[1]['cx']
    #        self.particles[1, :] += position[1] #- self.VPs[1]['cy']
            self.particles[1, :] += (2.55 - position[0])*3.2 #- self.VPs[1]['cx']
            self.particles[0, :] += (2.55 - position[1])*3.2 #- self.VPs[1]['cx']
            self.particles[2, :] += (2.55 - position[1])*3.2 #- self.VPs[1]['cx']

if __name__ == "__main__":
    import dot