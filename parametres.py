#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Projection information
----------------------
Les coordonnées dans la salle sont par convention définis par rapport à un plan de référence
 perpendiculaire à l'axe long de la salle:

- le point central  (0., 0., 0.) est le coin en bas à gauche de ce plan (donc leur position est positive: x,y,z > 0)
- l'axe x  perpendiculairement à ce plan, vers les VPs
- l'axe y court est l'axe transversal, horizontal
- l'axe z est la hauteur
- tout est physique, en mètres (29.7cm = 0.297m)

Par convention, la position spatiale des VPs par rapport au centre du plan de reference
- placement regulier en profondeur a equidistance du plan de ref (le long d'un mur)
- placement regulier, le centre en premier
- on place les VPs vers 1m30 de haut

Par convention, la position de la croix est au centre de la salle: [d_x/2, d_y/2]

"""

# pour savoir si on imprime des messages d'erreur
DEBUG  = False
DEBUG  = True

# taille de l'espace
#d_y, d_z = 4.9, 6.22*3/4
d_y, d_z = 6.6, 6.
d_x = 16.9 # en metres

# mesures au telemetre
from numpy import arctan2, pi
#largeur_ecran = 1.7 # ouvert à fond
# https://unspecified.wordpress.com/2012/06/21/calculating-the-gluperspective-matrix-and-other-opengl-matrix-maths/
#hauteur_ecran = 1.7*9./16. # ouvert à fond
#distance_ecran = 2.446
hauteur_ecran, distance_ecran  = 0.94, 2.58
# on calcule
foc_estim = 2 * arctan2(hauteur_ecran/2, distance_ecran) * 180 / pi # ref P101L1
#print foc_estim
foc =  foc_estim

volume = [d_x, d_y, d_z]

# scenario qui est joué par le modele physique
scenario = "fan" # une aura autour de la position du premier player
scenario = 'rotating-circle'
scenario = 'cristal'
scenario = "croix" # calibration autour de la croix
scenario = "leapfrog" # integration d'Euler améliorée pour simuler le champ

# et direction d'angle de vue (cx, cy, cz) comme le point de fixation ainsi que le champ de vue (en deg)
# distance des VPs du plan de reference
# profondeur du plan de référence
z = 1.36  # hauteur des VPs
cx_0, cx_1 = 0., d_x  # ->on positionne l'écran pour régler la visée au fond de la salle # d_x - 10.27
cy = d_y/2 # on regarde le centre du plan de reference
cz = z # d_z/2
# une liste des video projs donnant:
# leur adresse, port, leurs parametres physiques
VPs = [
        {'address':'10.42.0.56',
            'x':d_x, 'y':0.50, 'z': z,
            'cx':cx_0, 'cy':cy, 'cz': cz,
            'foc': foc, 'pc_min': 0.30, 'pc_max': 100},
        {'address':'10.42.0.55',
            'x':d_x, 'y':3.07, 'z': z,
            'cx':cx_0, 'cy':cy, 'cz': cz,
            'foc': foc, 'pc_min': 0.30, 'pc_max': 100},
        {'address':'10.42.0.54',
            'x':d_x, 'y':6.3, 'z': z,
            'cx':cx_0, 'cy':cy, 'cz': cz,
            'foc': foc, 'pc_min': 0.30, 'pc_max': 100},
        {'address':'10.42.0.51',
            'x':1.98, 'y':0.55, 'z': z,
            'cx':cx_1, 'cy':cy, 'cz': cz,
            'foc': foc, 'pc_min': 0.30, 'pc_max': 100},
        {'address':'10.42.0.52',
             'x':1.98, 'y':3.37, 'z': z,
             'cx':cx_1, 'cy':cy, 'cz': cz,
             'foc': foc, 'pc_min': 0.30, 'pc_max': 100},
        {'address':'10.42.0.53',
             'x':1.98, 'y':6.3, 'z': z,
             'cx':cx_1, 'cy':cy, 'cz': cz,
             'foc': foc, 'pc_min': 0.30, 'pc_max': 100},
        ]
import numpy as np
calibration = {
        'center': np.array([d_x/2., d_y/2, VPs[0]['z']], dtype='f'), # central point of the room  / point focal, pour lequel on optimise kinect et VPs?
        'croix': np.array([8.65, 3.67, 1.36], dtype='f'), # definition de la position de la croix
#        'croix': np.array([11.95, 2.2, 1.36], dtype='f'), # definition de la position de la croix
        'roger': np.array([d_x/2., d_y/2., 1.73], dtype='f'), #  fixation dot  (AKA Roger?)
                }

# parametres du champ
p = {'N': 32,
     # parametres perceptifs
     'distance_m': 0.50, # distance d'équilibre des segments autour d'une position de player
     'G_global': 3.0, # attraction globale vers les centres des positions
     'G_rot': 2.,
     'G_rot_hot': 5.,
     'distance_tabou': 0.2, # distance tabou
     'G_tabou': 0.5, # force tabou qui expulse tout segment qui rentre dans la zone tabou
     'G_gravite': 1.0, # parametre d'attraction physique vers les players
     # parametres physiques
     'G_poussee': .10, # parametre de poussee créateur de vortex
     'G_struct': .1, # force avec laquelle les bouts de segments s'attirent
     'G_struct_hot': .3, # force avec laquelle les bouts de segments s'attirent
     'distance_struct': .3, # distance pour laquelle li'attraction des bouts de segments s'inverse
     'distance_struct_hot': .8,
     'G_repulsion': 1.0, # constante de répulsion entre les particules
     'G_repulsion_hot': .5, # constante de répulsion entre les particules
     'eps': 1.e-4, # longueur (en metres) minimale pour eviter les overflows: ne doit pas avoir de qualité au niveau de la dynamique
     'G_spring': 3., 'l_seg_min': 0.4, 'l_seg_max': 2., # dureté et longueur des segments
     'G_spring_hot': 1., 'l_seg_hot': 2.,  # dureté et longueur des segments dans un break
     # parametres globaux
     'damp': .2,  # facteur de damping / absorbe l'énergie / regle la viscosité
     'damp_hot': .99,  # facteur de damping / absorbe l'énergie / regle la viscosité  / absorbe la péchitude
     'speed_0': .1, # facteur global (et redondant avec les G_*) pour régler la vitesse des particules
     'scale': 1., # facteur global régler la saturation de la force
     'kurt' : .0, # 1 is normal gravity, higher makes the attraction more local
     'line_width': 3, # line width of segments
     'T_break': 6., # duration (secondes) of all three breaks
     'A_break': 7.5, # amplitude du break #2 et #3
     'tau_break': .103, # duration du transient dans les breaks #2 et #3
}

from numpy import pi
#parametres des kinects
# une liste des kinects donnant leur adresse, port, position (x; y; z) et azimuth.
# pour des kinects dans le segment (0, d_y) --- (d_x, d_y) alors  az : 11*pi/6 = a gauche , 9*pi/6 = tout droit, 7*pi/6 = a droite
info_kinects = [
		# on tourne les numeros de kinect dans le sens des aiguilles d'une montre en commencant par
           #  le point (0, 0)- le point de vue (az) donne l'ordre dans une colonne de kinects
		# deuxieme  bloc
		{'address':'10.42.0.14', 'port': 9998, 'x':8.8, 'y':0.26, 'z': 1.24, 'az':pi/6 ,'max':560},#1.1
		{'address':'10.42.0.14', 'port': 9999, 'x':8.8, 'y':0.26, 'z': 1.14, 'az':3*pi/6 ,'max':560}, #1.2
		{'address':'10.42.0.15', 'port': 9998, 'x':8.8, 'y':0.26, 'z': 1.24, 'az':5*pi/6 ,'max':560},#1.3
		{'address':'10.42.0.15', 'port': 9999, 'x':14.2, 'y':0.26, 'z': 1.14, 'az':3*pi/6 ,'max':560},#1.3

#		# premier  bloc
        {'address':'10.42.0.17', 'port': 9998, 'x':3.8, 'y':0.26, 'z': 1.14, 'az':3*pi/6 ,'max':560},#2.1
#		{'address':'10.42.0.12', 'port': 9999, 'x':8.0, 'y':0, 'z': 1.24, 'az':5*pi/6 ,'max':497},#2.2
#		{'address':'10.42.0.13', 'port': 9998, 'x':8.0, 'y':d_y, 'z': 1.34, 'az':11*pi/6 ,'max':483},#2.3
#		{'address':'10.42.0.12', 'port': 9998, 'x':12.0, 'y':d_y, 'z': 1.14, 'az':9*pi/6 ,'max':483},#2.4

#		{'address':'10.42.0.12', 'port': 9998, 'x':8.8, 'y':d_y-0.19, 'z': 1.24, 'az':7*pi/6 ,'max':560},#1.1
#		{'address':'10.42.0.12', 'port': 9999, 'x':8.8, 'y':d_y-0.19, 'z': 1.14, 'az':9*pi/6 ,'max':500}, #1.2
#		{'address':'10.42.0.13', 'port': 9998, 'x':8.8, 'y':d_y-0.19, 'z': 1.24, 'az':11*pi/6 ,'max':560},#1.3
##		{'address':'10.42.0.13', 'port': 9999, 'x':14.2, 'y':d_y-0.19, 'z': 1.14, 'az':9*pi/6 ,'max':100},#1.3
#
##		# premier  bloc
#        {'address':'10.42.0.18', 'port': 9998, 'x':3.8, 'y':d_y-0.19, 'z': 1.14, 'az':9*pi/6 ,'max':500}#2.1
#		{'address':'10.42.0.12', 'port': 9999, 'x':8.0, 'y':0, 'z': 1.24, 'az':5*pi/6 ,'max':497},#2.2
#		{'address':'10.42.0.13', 'port': 9998, 'x':8.0, 'y':d_y, 'z': 1.34, 'az':11*pi/6 ,'max':483},#2.3
#		{'address':'10.42.0.12', 'port': 9998, 'x':12.0, 'y':d_y, 'z': 1.14, 'az':9*pi/6 ,'max':483},#2.4
		]

run_thread_network_config = {
    'port_to_line_res' : 8005,
    'ip_to_line_res' : "10.42.0.70",
}

kinects_network_config = {
    'UDP_IP' : "",
    'UDP_PORT' : 3003,
    'send_UDP_IP' : "10.42.0.100",
    'send_UDP_PORT' : 3005,
    'para_data' : [1 , 10, 50, 350, 5 ],
}
try:
    def sliders(p):
        import matplotlib as mpl
        mpl.rcParams['interactive'] = True
        mpl.rcParams['backend'] = 'macosx'
        mpl.rcParams['backend_fallback'] = True
        mpl.rcParams['toolbar'] = 'None'
        import pylab as plt
        fig = plt.figure(1)
        f_manager = plt.get_current_fig_manager()
        # f_manager.window.move(0, 0) does not work on MacOsX
        f_manager.set_window_title(" Quand c'est trop c'est tropico, COCO ")
        plt.ion()
        # turn interactive mode on for dynamic updates.  If you aren't in interactive mode, you'll need to use a GUI event handler/timer.
        from matplotlib.widgets import Slider as slider_pylab
        ax, value = [], []
        n_key = len(p.keys())*1.
    #    print s.p.keys()
        liste_keys = p.keys()
        liste_keys.sort()
        for i_key, key in enumerate(liste_keys):
            ax.append(fig.add_axes([0.15, 0.05+i_key/(n_key-1)*.9, 0.6, 0.05], axisbg='lightgoldenrodyellow'))
            if p[key] > 0:
                value.append(slider_pylab(ax[i_key], key, 0., (p[key] + (p[key]==0)*1.)*10, valinit=p[key]))
            elif p[key] < 0:
                value.append(slider_pylab(ax[i_key], key,  -(p[key] + (p[key]==0)*1.)*10, 0., valinit=p[key]))
            else:
                value.append(slider_pylab(ax[i_key], key,  -(p[key] + (p[key]==0)*1.)*10, (p[key] + (p[key]==0)*1.)*10, valinit=p[key]))

        def update(val):
            print '-'*80
            for i_key, key in enumerate(liste_keys):
                p[key]= value[i_key].val
                print key, p[key]#, value[i_key].val
            plt.draw()

        for i_key, key in enumerate(liste_keys): value[i_key].on_changed(update)
        plt.show(block=False) # il faut pylab.ion() pour pas avoir de blocage
        return fig
except Exception, e:
    print('problem while importing sliders ! Error = ', e)

if __name__ == "__main__":
    import sys
#    print sys.argv[0], str(sys.argv[1]), sys.argv[2] # nom du fichier, param1 , param2
    import display_modele_dynamique
    #sys.path.append('network')
    #import modele_dynamique_server

