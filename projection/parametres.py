# -*- coding: utf-8 -*-
#HACK
# N_Y, N_Z = 1240, 1024
#N_Y, N_Z = 960, 600 # enigma
#N_Y, N_Z = 960, 540 # monolithe
#N_Y, N_Z = 480, 300 # enigma


# Projection information
# ----------------------
# les coordonnées dans la salle sont par convention définis par rapport à un plan de référence
# perpendiculaire à l'axe long de la salle:
# le point central  (0., 0., 0.) est le coin en bas à gauche de ce plan (pratique, car au niveau des kinects :-) )
# l'axe x court perpendiculairement à ce plan, vers les VPs (donc leur position est positive: x > 0. )
# l'axe y est l'axe transversal, horizontal
# l'axe z est la hauteur
# tout est physique, en mètres

# taille du plan de reference
d_y, d_z = 4.54, 4.54*3/4
# distance des VPs du plan de reference
d_x = 8.5 # en metres

volume = [d_x, d_y, d_z]

# position spatiale des VPs par rapport au centre du plan de reference
# placement regulier en profondeur a equidistance du plan de ref (le long d'un mur)
# placement regulier, le centre en premier
# a place les VPs à  1m50 de haut


# une liste des video projs donnant:
# leur adresse, port, PAS UTILISE POUR LE MOMENT
# position (x; y; z) par rapport au centre de la pièce
# et direction d'angle de vue (cx, cy, cz) comme le point de fixation ainsi que le champ de vue (en deg)
VPs = [
        {'address':'127.0.0.1', 'port': 50034,
            'x':d_x, 'y':.5*d_y, 'z': 1.50, # au centre, à  1m50 de haut
            'cx':0., 'cy':d_y/2, 'cz': d_z/2, # on regarde le centre du plan de reference
            'foc': 30. },
        {'address':'127.0.0.1', 'port': 50035,
            'x':d_x, 'y':.1*d_y, 'z': 1.50, # a droite, à  1m50 de haut
            'cx':0., 'cy':d_y/2, 'cz': d_z/2, # on regarde le centre du plan de reference
            'foc': 30.  },
        {'address':'127.0.0.1', 'port': 50036,
            'x':d_x, 'y':.9*d_y, 'z': 1.50, # a gauche, à  1m50 de haut
            'cx':0., 'cy':d_y/2, 'cz': d_z/2, # on regarde le centre du plan de reference
            'foc': 30.  },
        ]
