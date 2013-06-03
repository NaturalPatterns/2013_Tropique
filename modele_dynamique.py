# -*- coding: utf-8 -*-
"""
Scenarios


"""

import numpy as np
import time

def arcdistance(rae1, rae2):
    """
    renvoie l'angle sur le grand cercle (en radians)

    # rae1 ---> rae2

     r = distance depuis le centre des coordonnées sphériques (mètres)
     a =  azimuth = declinaison = longitude (radians)
     e =  elevation = ascension droite = lattitude (radians)

    http://en.wikipedia.org/wiki/Great-circle_distance
    http://en.wikipedia.org/wiki/Vincenty%27s_formulae
    """
#    a = np.sin((azel[2, ...] - azel[0, ...])/2) **2 + np.cos(azel[0, ...]) * np.cos(azel[2, ...]) * np.sin((azel[3, ...] - azel[1, ...])/2) **2
#    return 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    a =  (np.cos(rae2[2, ...]) * np.sin(rae2[1, ...] - rae1[1, ...]))**2
    a += (np.cos(rae1[2, ...]) * np.sin(rae2[2, ...]) -  np.sin(rae1[2, ...]) *  np.cos(rae2[2, ...]) * np.cos(rae2[1, ...] - rae1[1, ...]))**2
    b =   np.sin(rae1[2, ...]) * np.sin(rae2[2, ...]) +  np.cos(rae1[2, ...]) *  np.cos(rae2[2, ...]) * np.cos(rae2[1, ...] - rae1[1, ...])
    return np.arctan2(np.sqrt(a), b)

def orientation(rae1, rae2):
    """
    renvoie le cap suivant le grand cercle (en radians)

     r = distance depuis le centre des coordonnées sphériques (mètres)
     a =  azimuth = declinaison = longitude (radians)
     e =  elevation = ascension droite = lattitude (radians)

     http://en.wikipedia.org/wiki/Great-circle_navigation
                #http://en.wikipedia.org/wiki/Haversine_formula
    """
    return np.arctan2(np.sin(rae2[1, ...] - rae1[1, ...]), np.cos(rae1[2, ...])*np.tan(rae2[2, ...]) - np.sin(rae1[2, ...])*np.cos(rae2[1, ...] - rae1[1, ...]))

def xyz2azel(xyz, OV = np.zeros((3,))):
    """
    renvoie le vecteur de coordonnées perceptuelles en fonction des coordonnées physiques

    xyz = 3 x N x ...

    Le vecteur OV désigne le centre des coordonnées sphériques,
    - O est la référence des coordonnées cartésiennes et
    - V les coordonnées cartesiennes du centre (typiquement du videoprojecteur).

    """
    rae = np.zeros(xyz.shape)
#     print rae.shape, xyz, VP
    if (rae.ndim > 1): OV = OV[:, np.newaxis]
    if (rae.ndim > 2): OV = OV[:, np.newaxis]
    rae[0, ...] = np.sqrt(np.sum((xyz - OV)**2, axis=0))
    rae[1, ...] = np.arctan2(xyz[1, ...] - OV[1], xyz[0, ...] - OV[0])
    rae[2, ...] = np.arctan2(xyz[2, ...] - OV[2], rae[0, ...])
    return rae

def rae2xyz(rae, OV = np.zeros((3,))):
    """
    renvoie le vecteur de coordonnées physiques en fonction des coordonnées perceptuelles

    """
    xyz = np.zeros(rae.shape)
    xyz[0, ...] = rae[0, ...] * np.cos(rae[2, ...])  * np.cos(rae[1, ...]) + OV[0]
    xyz[1, ...] = rae[0, ...] * np.cos(rae[2, ...])  * np.sin(rae[1, ...]) + OV[1]
    xyz[2, ...] = rae[0, ...] * np.sin(rae[2, ...]) + OV[2]
    return xyz


class Scenario:
    def __init__(self, N, scenario, volume, VPs, p, calibration):
        self.t = time.time()
        self.scenario = scenario
        self.volume = volume
        d_x, d_y, d_z = self.volume
        self.center = calibration['center'] # central point of the room  / point focal, pour lequel on optimise kinect et VPs?
        self.croix =  calibration['croix'] # definition de la position de la croix
        self.roger =  calibration['roger'] #  fixation dot  (AKA Roger?)
        self.VPs = VPs # le dictionnaire avec les characteristiques de tous les VPs
        self.vps = [] # la liste des VPs qui ont utilisés, et que ceux-là
        for VP in self.VPs:
            self.vps.append(np.array([VP['x'], VP['y'], VP['z']]))
        self.nvps = len(self.vps)
        self.p = p
        self.N = N
        self.l_seg = p['l_seg_min'] * np.ones(N)
        self.l_seg[-2:] = p['l_seg_max']
        self.order = 2

        # initialisation des particules
        self.particles = np.zeros((6*self.order, N), dtype='f') # x, y, z, u, v, w
        self.particles[0:3, :] = self.center[:, np.newaxis]
        self.particles[3:6, :] = self.center[:, np.newaxis]
        self.particles[1, :] = np.linspace(d_y/4, 3*d_y/4, self.N)
        self.particles[3:6, :] = self.particles[0:3, :] + np.random.randn(3, self.N)*self.l_seg
        self.particles[4, :] = self.particles[1, :]
        self.particles[5, :] -= self.l_seg
        self.t_break = 0.

    def champ(self, positions, events):
        if events[1] == 0 and not(events[:6] == [1, 1, 1, 1, 1, 1]): # event avec la touche P dans display_modele_dynamique.py
            self.l_seg[:-2] = self.p['l_seg_min'] * np.ones(self.N-2)
            self.l_seg[-2:] = self.p['l_seg_max']
            G_spring = self.p['G_spring']
            G_tabou = self.p['G_tabou']
            distance_tabou = self.p['distance_tabou']
        else:
            self.l_seg[:-2] = self.p['l_seg_hot'] * np.ones(self.N-2)
            self.l_seg[-6:] = self.p['l_seg_max']
            G_spring = self.p['G_spring_hot']
            G_tabou = self.p['G_tabou_event']
            distance_tabou = self.p['distance_tabou_event']
        if events[4] == 0  and not(events[:6] == [1, 1, 1, 1, 1, 1]): # event avec la touche G dans display_modele_dynamique.py
            G_rot = self.p['G_rot']
        else:
            G_rot = self.p['G_rot_hot']

        if events[2] == 0  and not(events[:6] == [1, 1, 1, 1, 1, 1]): # event avec la touche V dans display_modele_dynamique.py
            G_repulsion = self.p['G_repulsion']
        else:
            G_repulsion = self.p['G_repulsion_hot']
        if events[0] == 0  and not(events[:6] == [1, 1, 1, 1, 1, 1]): # event avec la touche R dans display_modele_dynamique.py
            G_struct = self.p['G_struct']
            distance_struct = self.p['distance_struct']
        else:
            G_struct = self.p['G_struct_hot']
            distance_struct = self.p['distance_struct_hot']

        # initialize t_break at the onset
        if (events[:6] == [1, 1, 1, 1, 1, 1]) and (self.t_break == 0.):
            self.t_break = self.t

        # reset the break after T_break seconds AND receiveing the restting signal
        if not(self.t_break == 0):# and (events[:6] == [0, 0, 0, 0, 0, 0]):
#             print self.t_break, self.t
            if (events[:6] == [0, 0, 0, 0, 0, 0]):
                if self.t > self.t_break + self.p['T_break']: self.t_break = 0.

        # TODO: simplifier le code pour garder les interactions principales
        force = np.zeros((6, self.N)) # one vector per point
        n = self.p['kurt']

        # FORCES SUBJECTIVES  dans l'espace perceptuel
        # TODO :  les répulsions combinéees avec l'attraction centripete crée un fan puis transition a plusieurs anneaux / rotation?
        # point C (centre) du segment
        OA = self.particles[0:3, :]
        OB = self.particles[3:6, :]
        OC = (OA+OB)/2
        for OV in self.vps[:]:
            rae_VC = xyz2azel(OC, OV)
            rae_VA = xyz2azel(self.particles[:3, :], OV) # 3 x N
            rae_VB = xyz2azel(self.particles[3:6, :], OV) # 3 x N

#            # attraction / repulsion des angles relatifs des segments
            if not(positions == None) and not(positions == np.nan):
                distance_min = 1.e6 * np.ones((self.N)) # very big to begin with
                rotation1 = np.empty((3, self.N))
                rotation2 = np.empty((3, self.N))
                gravity = np.empty((3, self.N))
                for position in positions:
                    rae_VS = xyz2azel(np.array(position), OV)
                    arcdis = np.min(np.vstack((arcdistance(rae_VS, rae_VA),\
                                               arcdistance(rae_VS, rae_VB),\
                                               arcdistance(rae_VS, rae_VC))), axis=0)
                    distance_SC = rae_VS[0]*np.sin(arcdis)
                    SC = OC - np.array(position)[:, np.newaxis]
                    SC_0 = SC / np.sqrt((SC**2).sum(axis=0)) # unit vector going from the player to the center of the segment

                    # TODO : diminuer la force du tabou dans le temps pour les personnes arrétées / parametre T_damp_global
                    tabou = - SC_0 * (distance_SC < distance_tabou) * (distance_SC**n - distance_tabou**n)/(distance_SC + self.p['eps'])**(n+2) # en metres
                    force[0:3, :] += G_tabou * tabou
                    force[3:6, :] += G_tabou * tabou

                    # TODO : réduire la dimension de profondeur à une simple convergence vers la position en x / reflète la perception
                    gravity_ = - SC_0 * (distance_SC**n - self.p['distance_m']**n)/(distance_SC + self.p['eps'])**(n+2) # en metres

                    # compute desired rotation
                    #cap_SC = orientation(rae_VS, rae_VC)
                    #cap_AB = orientation(rae_VA, rae_VB)

                    # TODO rotation aussi vers le plan perpendiculaire a l'acteur
                    # TODO résoudre le hack avec sign_view
                    # TODO : tuner les paramètres de rotation
                    #AB = self.particles[3:6, :] - self.particles[0:3, :]# 3 x N
#                    print np.sum(AB**2, axis=0)
                    #sign_view = np.sign(OC[0]-OV[0])
                    #rotation_ = -sign_view * np.sin(cap_SC-cap_AB)[np.newaxis, :] * np.vstack((AB[0, :], -AB[2, :], AB[1, :])) / np.sqrt(np.sum(AB**2, axis=0) + self.p['eps']**2) #
                    rotation_1 = OC + distance_SC * SC_0 - OA
                    rotation_2 = OC + (distance_SC + self.l_seg)  * SC_0 - OB
                    # print sign_view * np.sin(cap_SC-cap_AB)
                    # only assign on the indices that correspond to the minimal distance
                    ind_assign = (distance_SC < distance_min)
                    gravity[:, ind_assign] = gravity_[:, ind_assign]
                    rotation1[:, ind_assign] = rotation_1[:, ind_assign]
                    rotation2[:, ind_assign] = rotation_2[:, ind_assign]
                    distance_min[ind_assign] = distance_SC[ind_assign]

                force[0:3, :] += self.p['G_global'] / self.nvps * gravity
                force[3:6, :] += self.p['G_global'] / self.nvps * gravity
                force[0:3, :] += G_rot / self.nvps * rotation1
                force[3:6, :] -= G_rot / self.nvps * rotation2

        # FORCES GLOBALES  dans l'espace physique

        # TODO :  gravité vers le bas pour séparer 2 phases
        if not(self.p['G_gravite'] == 0.) or not(G_rot == 0.):
            if not(positions == None) and not(positions == np.nan):
                distance_min = 1.e6 * np.ones((self.N)) # very big to begin with
                rotation1 = np.empty((3, self.N))
                rotation2 = np.empty((3, self.N))
                gravity = np.empty((3, self.N))
                for position in positions:
                    # point C (centre) du segment
                    SC = (self.particles[0:3, :]+self.particles[3:6, :])/2-np.array(position)[:, np.newaxis]
                    distance_SC = np.sqrt(np.sum(SC**2, axis=0)) # en metres
                    SC_0 = SC / distance_SC # unit vector going from the player to the center of the segment
                    gravity = - SC_0 * (distance_SC**n - self.p['distance_m']**n)/(distance_SC + self.p['eps'])**(n+2) # en metres

                    rotation_1 = OC + distance_SC * SC_0 - OA
                    rotation_2 = OC + (distance_SC + self.l_seg)  * SC_0 - OB

                    ind_assign = (distance_SC < distance_min)
                    gravity[:, ind_assign] = gravity_[:, ind_assign]
                    rotation1[:, ind_assign] = rotation_1[:, ind_assign]
                    rotation2[:, ind_assign] = rotation_2[:, ind_assign]
                    distance_min[ind_assign] = distance_SC[ind_assign]

#                force[0:3, :] += self.p['G_gravite'] * gravity
#                force[3:6, :] += self.p['G_gravite'] * gravity
                force[0, :] += self.p['G_gravite'] * gravity[0]
                force[3, :] += self.p['G_gravite'] * gravity[0]
                #force[0:3, :] += G_rot * rotation1
                #force[3:6, :] += G_rot * rotation2

        ## forces entres les particules
        #OC = (self.particles[0:3, :]+self.particles[3:6, :])/2
        CC = OC[:, :, np.newaxis]-OC[:, np.newaxis, :] # 3xNxN ; en metres
        if not(G_repulsion==0.):
            # repulsion entre les centres de de chaque paire de segments
            distance = np.sqrt(np.sum(CC**2, axis=0)) # NxN ; en metres
            gravity = - np.sum(CC**n/(distance.T + self.p['eps'])**(n+2), axis=1) # 3 x N; en metres
            force[0:3, :] += G_repulsion * gravity
            force[3:6, :] += G_repulsion * gravity
            # TODO attraction / repulsion des angles relatifs des segments

        if not(self.p['G_poussee']==0.):
            distance = np.sqrt(np.sum(CC**2, axis=0)) # NxN ; en metres
            # poussee entrainant une rotation lente et globale (cf p152)
            ind_min = np.argmin(distance + np.eye(self.N)*1e6, axis=0)
            speed_CC = (self.particles[6:9, :] + self.particles[6:9, ind_min]) + (self.particles[9:12, :] + self.particles[9:12, ind_min])
            poussee =  np.sign(np.sum(speed_CC * CC[:,ind_min,:].diagonal(axis1=1, axis2=2), axis=0)) * CC[:,ind_min,:].diagonal(axis1=1, axis2=2) /(distance[:,ind_min].diagonal() + self.p['eps'])**(n+2) # 3 x N; en metres
            force[0:3, :] += self.p['G_poussee'] * poussee
            force[3:6, :] += self.p['G_poussee'] * poussee

        # attraction des extremites des segments au dessous d'une distance
        # critique pour créer des clusters de lignes
        if not(G_struct==0.):
            AA_ = self.particles[0:3, :, np.newaxis]-self.particles[0:3, np.newaxis, :]
            distance = np.sqrt(np.sum(AA_**2, axis=0)) # NxN ; en metres
            gravity = - np.sum((distance < distance_struct) * AA_ /(distance.T + self.p['eps'])**3, axis=1) # 3 x N; en metres
            force[0:3, :] += G_struct * gravity
            AB_ = self.particles[3:6, :, np.newaxis]-self.particles[3:6, np.newaxis, :]
            distance = np.sqrt(np.sum(AB_**2, axis=0)) # NxN ; en metres
            gravity = - np.sum((distance < distance_struct) * AB_/(distance.T + self.p['eps'])**3, axis=1) # 3 x N; en metres
            force[3:6, :] += G_struct * gravity
            BB_ = self.particles[0:3, :][:, :, np.newaxis]-self.particles[3:6, :][:, :, np.newaxis]
            distance = np.sqrt(np.sum(BB_**2, axis=0)) # NxN ; en metres
            gravity = - np.sum((distance < distance_struct) * BB_/(distance.T + self.p['eps'])**3, axis=1) # 3 x N; en metres
            force[0:3, :] += .5 * G_struct * gravity
            force[3:6, :] += .5 * G_struct * gravity
            # print G_struct, G_rot, G_repulsion

        # ressort
        AB = self.particles[0:3, :]-self.particles[3:6, :] # 3 x N
        distance = np.sqrt(np.sum(AB**2, axis=0)) # en metres
        force[0:3, :] -= G_spring * (distance[np.newaxis, :] - self.l_seg) * AB / (distance[np.newaxis, :] + self.p['eps'])
        force[3:6, :] += G_spring * (distance[np.newaxis, :] - self.l_seg) * AB / (distance[np.newaxis, :] + self.p['eps'])

        # damping
        if events[7] == 1  and not(events[:6] == [1, 1, 1, 1, 1, 1]): # event avec la touche S dans display_modele_dynamique.py
            force -= self.p['damp_hot'] * self.particles[6:12, :]/self.dt
        else:
            force -= self.p['damp'] * self.particles[6:12, :]/self.dt

        # normalisation des forces pour éviter le chaos
        if not(self.t_break == 0):# and (events[:6] == [0, 0, 0, 0, 0, 0]):
            if (events[-1] == 0): # break #2 or #3
                if self.t > self.t_break + self.p['T_break']:
                    speed_0 = self.p['speed_0']
                else:
                    speed_0 = self.p['speed_0'] *((self.p['A_break']-1) * np.exp(-(self.p['T_break'] - (self.t - self.t_break)) / self.p['tau_break']) + 1)
#                     print speed_0
            else:
                speed_0 = self.p['speed_0']
        else:
            speed_0 = self.p['speed_0']

        force = self.p['scale'] * np.tanh(force/self.p['scale'])
        force *= speed_0
        return force

    def do_scenario(self, positions=None, events=[0, 0, 0, 0, 0, 0, 0, 0]):
        self.t_last = self.t
        self.t = time.time()
        self.dt = (self.t - self.t_last)
        d_x, d_y, d_z = self.volume


        if self.scenario == 'croix':

            longueur_segments = .8

            # ligne horizontale
            self.particles[0, :self.N/2] = self.croix[0] # on the reference plane
            self.particles[1, :self.N/2] = self.croix[1]
            self.particles[2, :self.N/2] = self.croix[2] - longueur_segments/2.
            self.particles[3, :self.N/2] = self.croix[0] # on the reference plane
            self.particles[4, :self.N/2] = self.croix[1]
            self.particles[5, :self.N/2] = self.croix[2] + longueur_segments/2.
            # ligne verticale
            self.particles[0, self.N/2:] = self.croix[0] # on the reference plane
            self.particles[1, self.N/2:] = self.croix[1] - longueur_segments/2.
            self.particles[2, self.N/2:] = self.croix[2]
            self.particles[3, self.N/2:] = self.croix[0] # on the reference plane
            self.particles[4, self.N/2:] = self.croix[1] + longueur_segments/2.
            self.particles[5, self.N/2:] = self.croix[2]

        elif self.scenario == 'calibration':
            longueur_segments, undershoot_z = .05, .0

            # ligne horizontale
            self.particles[0, :self.N/2] = self.center[0] # on the reference plane
            self.particles[1, :self.N/2] = np.linspace(0, d_y, self.N/2)
            self.particles[2, :self.N/2] = self.center[2] - longueur_segments/2. - undershoot_z
            self.particles[3, :self.N/2] = self.center[0] # on the reference plane
            self.particles[4, :self.N/2] = np.linspace(0, d_y, self.N/2)
            self.particles[5, :self.N/2] = self.center[2] + longueur_segments/2. - undershoot_z
            # ligne verticale
            self.particles[0, self.N/2:] = self.center[0] # on the reference plane
            self.particles[1, self.N/2:] = self.center[1] - longueur_segments/2.
            self.particles[2, self.N/2:] = np.linspace(0, d_z, self.N/2) - undershoot_z
            self.particles[3, self.N/2:] = self.center[0] # on the reference plane
            self.particles[4, self.N/2:] = self.center[1] + longueur_segments/2.
            self.particles[5, self.N/2:] = np.linspace(0, d_z, self.N/2) - undershoot_z
            #            print self.particles.mean(axis=1)

        elif self.scenario == 'cristal':
            #             self.particles = 1000*np.ones((6, self.N)) # segments outside
            frequency_plane = .005 # how fast the whole disk moves in Hz
            length = .5 # length of each AB
            mean_elevation, frequency_elevation, std_elevation = 90. * np.pi / 180., 0.3, 45. * np.pi / 180.  # elevation (in radians) of viual angle for the points of convergence defiing the cristal's circle
            radius = 1.5 # convergence happens on a circle defined as the section of sphere of radius=radius and the elevation

            N_dots = self.N # np.min(16, self.N) # number of segments
            angle = 2 * np.pi * frequency_plane * self.t + np.linspace(0, 2 * np.pi, N_dots)
            elevation = mean_elevation + std_elevation * np.sin(2 * np.pi * frequency_elevation * self.t)

            self.particles[0, :N_dots] = radius*np.cos(elevation)
            self.particles[1, :N_dots] = radius*np.sin(elevation) * np.sin(angle)
            self.particles[2, :N_dots] = radius*np.sin(elevation) * np.cos(angle)
            self.particles[3, :N_dots] = (radius+length)*np.cos(elevation)
            self.particles[4, :N_dots] = (radius+length)*np.sin(elevation) * np.sin(angle)
            self.particles[5, :N_dots] = (radius+length)*np.sin(elevation) * np.cos(angle)
            self.particles[0:3, :] += np.array(positions[0])[:, np.newaxis]
            self.particles[3:6, :] += np.array(positions[0])[:, np.newaxis]


        elif self.scenario == 'fan':
            self.particles = np.zeros(self.particles.shape)
            frequency_plane = .005 # how fast the disk moves in Hz
            radius_min, radius_max = 2.0, 5.0
            radius, length_ratio = .2 * d_z, 1.4
            N_dots = 16 #np.min(16, self.N)

#            N_dots = 50
#            radius, length_ratio = .1 * d_z, 2
            angle = 2 * np.pi * frequency_plane * self.t + np.linspace(0, 2 * np.pi, N_dots)

            # a circle drawn on a rotating plane
            self.particles[0, :N_dots] = self.center[0] #+ radius #* np.sin(angle) #* np.sin(2*np.pi*frequency_rot*self.t)
            self.particles[1, :N_dots] = self.center[1] + radius * np.sin(angle) #* np.cos(2*np.pi*frequency_rot*self.t)
            self.particles[2, :N_dots] = self.center[2] + radius * np.cos(angle)
            self.particles[3, :N_dots] = self.center[0] #+ radius * length_ratio  #* np.sin(angle) #* np.sin(2*np.pi*frequency_rot*self.t)
            self.particles[4, :N_dots] = self.center[1] + radius * length_ratio * np.sin(angle) #* np.cos(2*np.pi*frequency_rot*self.t)
            self.particles[5, :N_dots] = self.center[2] + radius * length_ratio * np.cos(angle)
#            self.particles[0:3, N_dots:] = self.origin[:, np.newaxis] # un rayon vers l'origine
#            self.particles[3:6, N_dots:] = self.origin[:, np.newaxis] + .0001 # très fin

        elif self.scenario == '2fan':
            self.particles = np.zeros(self.particles.shape)
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
            self.particles[0:3, N_dots:] = self.center[:, np.newaxis] # un rayon vers l'origine
            self.particles[3:6, N_dots:] = self.center[:, np.newaxis] + .0001 # très fin

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
            self.particles[3, :N_dots] = self.center[0] + radius * length_ratio * np.sin(angle) * np.sin(2*np.pi*frequency_rot*self.t)
            self.particles[4, :N_dots] = self.center[1] + radius * length_ratio * np.sin(angle) * np.cos(2*np.pi*frequency_rot*self.t)
            self.particles[5, :N_dots] = self.center[2] + radius * length_ratio * np.cos(angle)
            self.particles[0:3, N_dots:] = self.center[:, np.newaxis] # un rayon vers l'origine
            self.particles[3:6, N_dots:] = self.center[:, np.newaxis] + .0001 # très fin

        elif self.scenario == 'odyssey':
            np.random.seed(12345)
            up_down = np.sign(np.random.randn(self.N)-.5)
            speed_flow, frequency_flow_trans = 20., .01 # how fast the whole disk moves in Hz
            frequency_plane_1, frequency_plane_2 = .0101, .01 # how fast the whole disk moves in Hz
#            frequency_rot_1, frequency_rot_2 = .02, .01 # how fast the whole disk moves in Hz
            radius, length, width = .3 * d_z, .8, d_y*4

            angle = 2 * np.pi * frequency_plane_1 * self.t
#            angle_rot_1 = 2 * np.pi * (frequency_rot_1 * self.t)+ np.ones(self.N)# + np.random.rand(self.N))
#            angle_rot_2 = 2 * np.pi * (frequency_rot_2 * self.t)+ np.ones(self.N)# + np.random.rand(self.N))

            # coordinates before the plane rotation
            #            x = d_x * np.sin(2*np.pi*frequency_flow*self.t)
#            x = np.mod(np.random.rand(self.N)*d_x + speed_flow*self.t, d_x)
            dx = -2*np.abs((np.linspace(0, d_x, self.N)-d_x/2))
            x = np.mod(dx + speed_flow*self.t, 3*d_x)
            y = np.linspace(-width/2, width/2, self.N) # np.random.rand(self.N)*width - width/2 #
            z = d_z / 5. * up_down
            l = np.sqrt(y**2 + z**2)
#            vector = np.array([np.zeros(self.N), y/l, z/l ])
#
#            self.particles[0, :] = x
#            self.particles[1, :] = y
#            self.particles[2, :] = z
#
#            self.particles[0:3, :] -= length/2. * vector
#            self.particles[3:6, :] += length/2. * vector
#
            # a circle drawn on a rotating plane
            self.particles[0, :] = x
            self.particles[1, :] = (y - y*length/l) * np.sin(angle) + (z - z*length/l) * np.cos(angle)
            self.particles[2, :] = (y - y*length/l) * np.cos(angle) - (z - z*length/l) * np.sin(angle)
#            self.particles[3:6, :] = self.particles[0:3, :]
            self.particles[3, :] = x
            self.particles[4, :] = (y + y*length/l) * np.sin(angle) + (z + z*length/l) * np.cos(angle)
            self.particles[5, :] = (y + y*length/l) * np.cos(angle) - (z + z*length/l) * np.sin(angle)

#            vector = np.array([np.cos(angle_rot_2)*np.cos(angle_rot_1), np.cos(angle_rot_2)*np.sin(angle_rot_1), np.sin(angle_rot_2) ])
#            vector = np.array([np.sin(angle_rot_2), np.cos(angle_rot_2)*np.cos(angle_rot_1), np.cos(angle_rot_2)*np.sin(angle_rot_1) ])
#            l = np.sqrt(self.particles[1, :]**2 + self.particles[2, :]**2)
#            vector = np.array([np.zeros(self.N), self.particles[2, :]/l, self.particles[1, :]/l ])

#            self.particles[0:3, :] -= length/2. * vector
#            self.particles[3:6, :] += length/2. * vector

            self.particles[0:3, :] += self.center[:, np.newaxis]
            self.particles[3:6, :] += self.center[:, np.newaxis]

        elif self.scenario == 'snake':
            np.random.seed(12345)
            up_down = np.sign(np.random.randn(self.N)-.5)
            speed_flow, frequency_flow_trans = 1., .01 # how fast the whole disk moves in Hz
            frequency_plane_1, frequency_plane_2 = .0101, .01 # how fast the whole disk moves in Hz
            #            frequency_rot_1, frequency_rot_2 = .02, .01 # how fast the whole disk moves in Hz
            radius, length, width = .3 * d_z, .8, d_y/4

            angle = 2 * np.pi * frequency_plane_1 * self.t
            #            angle_rot_1 = 2 * np.pi * (frequency_rot_1 * self.t)+ np.ones(self.N)# + np.random.rand(self.N))
            #            angle_rot_2 = 2 * np.pi * (frequency_rot_2 * self.t)+ np.ones(self.N)# + np.random.rand(self.N))

            # coordinates before the plane rotation
            #            x = d_x * np.sin(2*np.pi*frequency_flow*self.t)
            #            x = np.mod(np.random.rand(self.N)*d_x + speed_flow*self.t, d_x)
            #dx = -2*np.abs((np.linspace(0, d_x, self.N)-d_x/2))
#            x = np.mod(np.linspace(0, d_x, self.N) + speed_flow*self.t, d_x)
            x = d_x/2+np.sin(np.linspace(0, 2*np.pi, self.N)/3 + speed_flow*self.t) * d_x/2
            y = np.sin(np.linspace(0, 2*np.pi, self.N)/4) * width # np.random.rand(self.N)*width - width/2 #

            z = d_z / 5. #* up_down
            l = np.sqrt(y**2 + z**2)
            self.particles[0, :] = x
            self.particles[1, :] = y * np.sin(angle) + z * np.cos(angle)
            self.particles[2, :] = y * np.cos(angle) - z * np.sin(angle)

            self.particles[3:6, :] = np.roll(self.particles[0:3, :], 1, axis=1)
            self.particles[3:6, 0] = self.particles[0:3, 0]

            self.particles[0:3, :] += self.center[:, np.newaxis]
            self.particles[3:6, :] += self.center[:, np.newaxis]

        elif self.scenario == 'leapfrog':
            #            distance = np.sqrt((np.array(positions) - self.positions_old)**2).sum()
            #TODO : use simpy
            self.particles[:6, :] += self.particles[6:12, :] * self.dt/2
            force = self.champ(positions=positions, events=events)
            self.particles[6:12, :] += force * self.dt
            # TODO normalize spped?
            # application de l'acceleration calculée sur les positions
            self.particles[:6, :] += self.particles[6:12, :] * self.dt/2
#            self.positions_old = np.array(positions)

        elif self.scenario == 'euler':
            force = self.champ(positions=positions, events=events)
            self.particles[6:12, :] += force * self.dt
            # application de l'acceleration calculée sur les positions
            self.particles[:6, :] += self.particles[6:12, :] * self.dt

#         # routines on the position
#         if not(positions==None) and not(positions==np.nan) :
#             for position in positions:
#                 for VP in self.VPs:
#                     # TODO : fonction tabou dans les scenarios: zone d'évitement des bords: passer en coordonnées perceptuelles / utiliser la position des VPs / utiliser la position des VPs
#                     A=1
#
#

        # pour les scenarios de controle du suivi, on centre autour de la position du premier player
        if not(positions == None) and not(positions == np.nan) and not(positions == []) and (self.scenario in ['croix', 'fan', '2fan', 'rotating-circle', 'calibration']): #
            # pour la calibration on centre le pattern autour de la premiere personne captée
            self.particles[0:3, :] -= self.croix[:, np.newaxis]
            self.particles[3:6, :] -= self.croix[:, np.newaxis]
            self.particles[0:3, :] += np.array(positions[0])[:, np.newaxis]
            self.particles[3:6, :] += np.array(positions[0])[:, np.newaxis]


        # todo : éviter plaquage le long des bords
        #  permet de ne pas sortir du volume (todo: créer un champ répulsif aux murs...)
        if (self.scenario == 'leapfrog') or (self.scenario == 'euler') :
            for i in range(6):
                self.particles[i, (self.particles[i, :] < -1*self.volume[i % 3]) ] = -1*self.volume[i % 3]
                self.particles[i, (self.particles[i, :] > 2* self.volume[i % 3]) ] = 2*self.volume[i % 3]
                #self.particles[i, (self.particles[i, :] > self.volume[i % 3]) ] = self.volume[i % 3]
                #self.particles[i, (self.particles[i, :] < -.0*self.volume[i % 3]) ] = -.0*self.volume[i % 3]


if __name__ == "__main__":
    import display_modele_dynamique
