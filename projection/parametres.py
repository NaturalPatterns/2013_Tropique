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

"""
# taille de l'espace
#d_y, d_z = 4.9, 6.22*3/4
d_y, d_z = 6.26, 6.
d_x = 13.43 # en metres

# mesures au telemetre
z = 1.31# hauteur des VPs
from numpy import arctan2, pi
largeur_ecran = 1.75 # ouvert à fond
distance_ecran = 2.58
foc_estim = 2 * arctan2(largeur_ecran/2, distance_ecran) * 180 / pi # ref P101L1
foc_estim = 30.1
#foc = 72
foc = foc_estim
print("parameres.py nous dit: focale estimée = ", foc_estim, ", focal utilisée = ", foc)

volume = [d_x, d_y, d_z]

play = "leapfrog"
#play = "croix" # calibration croix a x=0, y =d_y/2, z = 1.36


# et direction d'angle de vue (cx, cy, cz) comme le point de fixation ainsi que le champ de vue (en deg) 
# distance des VPs du plan de reference
#profondeur du plan de référence
cx = 0# ->on positionne l'écran pour régler la visée au fond de la salle # d_x - 10.27
cy = d_y/2 # on regarde le centre du plan de reference
cz = z # d_z/2
# une liste des video projs donnant:
# leur adresse, port, leurs parametres physiques
# TODO: ne mettre que les VPs qui sont utilisés
VPs = [
        {'address':'10.42.0.51', 'port': 50035,
            'x':d_x, 'y':5.3, 'z': z,
            'cx':cx, 'cy':cy, 'cz': cz,
            'foc': foc, 'pc_min': 0.01, 'pc_max': 10000  },
        {'address':'10.42.0.52', 'port': 50034,
            'x':d_x, 'y':2.58, 'z': z,
            'cx':cx, 'cy':cy, 'cz': cz,
            'foc': foc, 'pc_min': 0.01, 'pc_max': 10000 },
        {'address':'10.42.0.53', 'port': 50036,
            'x':d_x, 'y':0, 'z': z,
            'cx':cx, 'cy':cy, 'cz': cz,
            'foc': foc, 'pc_min': 0.01, 'pc_max': 10000  },
        ]

# parametres du champ
p = {'N': 32,
#     'distance_m': 1.2, # distance d'équilibre des segments autour d'une position de player	
     'distance_m': 0.50, # distance d'équilibre des segments autour d'une position de player	
     'G_global': 40., # attraction globale vers les centres des positions
#      'G_rot': 1.0,
      'G_rot': 15.,
      'G_rot_hot': -.05,
#     'G_struct': 15.0,
     'distance_tabou': .9, # distance tabou
     'distance_tabou_event': .93, # distance tabou
     'G_tabou': 41.0, # force tabou qui expulse tout segment qui rentre dans la zone tabou
     'G_tabou_event': 500.0, # force tabou qui expulse tout segment qui rentre dans la zone tabou

     'G_poussee': 1., # force avec laquelle les bouts de segments s'attirent
     'G_struct': .1, # force avec laquelle les bouts de segments s'attirent
     'G_struct_hot': -1.3, # force avec laquelle les bouts de segments s'attirent
     'distance_struct': .3, # distance pour laquelle les bouts de segments s'attirent
     'distance_struct_hot': .8, # distance pour laquelle les bouts de segments s'attirent
     'G_repulsion': 2., # constante de répulsion entre les particules
     'G_repulsion_hot': -.5, # constante de répulsion entre les particules
#     'G_repulsion': 1.9, # constante de répulsion entre les particules
#     'G_repulsion': .001, # constante de répulsion entre les particules
     'eps': 1.e-2, # longueur (en metres) minimale pour eviter les overflows: ne doit pas avoir de qualité au niveau de la dynamique
     'G_gravite': 4., # force de gravité vers le bas de la piece
#     'G_spring': 20., 'l_seg': 0.3, # dureté et longueur des segments
     'G_spring': 5., 'l_seg_min': 0.6, 'l_seg_max': 4., # dureté et longueur des segments
     'G_spring_hot': 1., 'l_seg_hot': 2.,  # dureté et longueur des segments dans un break
     # parametres globaux
     'damp': .05,  # facteur de damping / absorbe l'énergie / regle la viscosité  / absorbe la péchitude
     'damp_hot': .99,  # facteur de damping / absorbe l'énergie / regle la viscosité  / absorbe la péchitude
#      'damp': .06,  # facteur de damping / absorbe l'énergie / regle la viscosité 
#     'speed_0': .9, # facteur global (et redondant avec les G_*) pour régler la vitesse des particules###
     'speed_0': 1., # facteur global (et redondant avec les G_*) pour régler la vitesse des particules
     'scale': 200., # facteur global (et redondant avec les G_*) pour régler la saturation dela force
#     'speed_0': .9, 
     'kurt' : 1., # 1 is normal gravity, higher makes the attraction more local
     'line_width': 3, # line width of segments
     'T_break': 6., # duration (secondes) of all three breaks
     'A_break': 7.5, # amplitude du break #2 et #3
     'tau_break': .103, # duration du transient dans les breaks #2 et #3
     }

#parametres des kinects
# une liste des kinects donnant leur adresse, port, position (x; y; z) et azimuth. 
info_kinects = [
#		{'address':'10.42.0.10', 'port': 9998, 'x':4.0, 'y':d_y, 'z': 1.3, 'az':7*pi/6 ,'max':520},#0
#		{'address':'10.42.0.10', 'port': 9999, 'x':4.0, 'y':d_y, 'z': 1.3, 'az':9*pi/6 ,'max':520},#1
		{'address':'10.42.0.11', 'port': 9998, 'x':1.6, 'y':d_y, 'z': 1.3, 'az':11*pi/6 ,'max':530},#2
		{'address':'10.42.0.11', 'port': 9999, 'x':1.6, 'y':d_y, 'z': 1.3, 'az':9*pi/6 ,'max':530},#3
		{'address':'10.42.0.12', 'port': 9998, 'x':8.4, 'y':d_y, 'z': 1.3, 'az':11*pi/6 ,'max':470},#4
		{'address':'10.42.0.12', 'port': 9999, 'x':11.2, 'y':d_y, 'z': 1.3, 'az':9*pi/6 ,'max':530},#5
		{'address':'10.42.0.13', 'port': 9998, 'x':8.4, 'y':d_y, 'z': 1.3, 'az':9*pi/6 ,'max':530},#6
		{'address':'10.42.0.13', 'port': 9999, 'x':8.4, 'y':d_y, 'z': 1.3, 'az':7*pi/6 ,'max':530},#7
#		{'address':'10.42.0.14', 'port': 9998, 'x':9.0, 'y':0, 'z': 1.3, 'az':3*pi/6 ,'max':490},#8
#  		{'address':'10.42.0.14', 'port': 9999, 'x':9.0, 'y':0, 'z': 1.3, 'az':5*pi/6 ,'max':505},#9
#		{'address':'10.42.0.15', 'port': 9998, 'x':100.0, 'y':0, 'z': 1.3, 'az':0 ,'max':491},#10
#		{'address':'10.42.0.15', 'port': 9999, 'x':100.0, 'y':0, 'z': 1.3, 'az':-1.2 ,'max':491},#11
#		{'address':'10.42.0.16', 'port': 9998, 'x':500.0, 'y':0, 'z': 1.3, 'az':0 ,'max':501},#4
#		{'address':'10.42.0.16', 'port': 9999, 'x':500.0, 'y':0, 'z': 1.3, 'az':+1.2 ,'max':497},#5
#		{'address':'10.42.0.17', 'port': 9998, 'x':100.0, 'y':0, 'z': 1.3, 'az':+1.2 ,'max':483},#6
#		{'address':'10.42.0.17', 'port': 9999, 'x':100.0, 'y':0, 'z': 1.3, 'az':0 ,'max':487},#7
#		{'address':'10.42.0.18', 'port': 9998, 'x':100.0, 'y':0, 'z': 1.3, 'az':-1.2 ,'max':490},#8
#  		{'address':'10.42.0.18', 'port': 9999, 'x':500.0, 'y':0, 'z': 1.3, 'az':0 ,'max':505},#9
#		{'address':'10.42.0.19', 'port': 9998, 'x':100.0, 'y':0, 'z': 1.3, 'az':0 ,'max':491},#10
#		{'address':'10.42.0.19', 'port': 9999, 'x':100.0, 'y':0, 'z': 1.3, 'az':-1.2 ,'max':491},#11
		]

run_thread_network_config = {
    'port_to_line_res' : 8005,
    'ip_to_line_res' : "10.42.0.70",
}

kinects_network_config = {
    'UDP_IP' : "",
    'UDP_PORT' : 3003,
#    'send_UDP_IP' : "10.42.0.1",
    'send_UDP_IP' : "10.42.0.100",
    'send_UDP_PORT' : 3005,
    'para_data' : [1 , 10, 50, 350, 5 ],
}
DEBUG  = False



if __name__ == "__main__":
    import explore
