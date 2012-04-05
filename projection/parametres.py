# -*- coding: utf-8 -*-
"""
Projection information
----------------------
Les coordonnées dans la salle sont par convention définis par rapport à un plan de référence
 perpendiculaire à l'axe long de la salle:

- le point central  (0., 0., 0.) est le coin en bas à gauche de ce plan (pratique, car au niveau des kinects :-) )
- l'axe x court perpendiculairement à ce plan, vers les VPs (donc leur position est positive: x > 0. )
- l'axe y est l'axe transversal, horizontal
- l'axe z est la hauteur
- tout est physique, en mètres

La position spatiale des VPs par rapport au centre du plan de reference
- placement regulier en profondeur a equidistance du plan de ref (le long d'un mur)
- placement regulier, le centre en premier
- on place les VPs vers 1m50 de haut

"""
# mesures au telemetre
z = 1.36 # hauteur des VPs
#foc = 30
from numpy import arctan2, pi
largeur_ecran = 1.21 # fermé à fond
distance_ecran = 2.82
foc = 2 * arctan2(largeur_ecran/2, distance_ecran) * 180 / pi # 
# taille du plan de reference
d_y, d_z = 4.54, 4.54*3/4
# distance des VPs du plan de reference
d_x = 11.30 # en metres

volume = [d_x, d_y, d_z]


# une liste des video projs donnant:
# leur adresse, port, PAS UTILISE POUR LE MOMENT
# position (x; y; z) par rapport au centre de la pièce
# et direction d'angle de vue (cx, cy, cz) comme le point de fixation ainsi que le champ de vue (en deg)
VPs = [
        {# 'address':'127.0.0.1', 'port': 50035,
            'x':d_x, 'y':2.03, 'z': z, # a droite, à  1m50 de haut
            'cx':0., 'cy':d_y/2, 'cz': d_z/2, # on regarde le centre du plan de reference
            'foc': foc, 'pc_min': 0.01, 'pc_max': 10000  },
        {# 'address':'127.0.0.1', 'port': 50034,
            'x':d_x, 'y':0., 'z': z, # au centre, à  1m50 de haut
            'cx':0., 'cy':d_y/2, 'cz': d_z/2, # on regarde le centre du plan de reference
            'foc': foc, 'pc_min': 0.01, 'pc_max': 10000 },
        {# 'address':'127.0.0.1', 'port': 50036,
            'x':d_x, 'y':3.87, 'z': z, # a gauche, à  1m50 de haut
            'cx':0., 'cy':d_y/2, 'cz': d_z/2, # on regarde le centre du plan de reference
            'foc': foc, 'pc_min': 0.01, 'pc_max': 10000  },
        {# 'address':'127.0.0.1', 'port': 50037,
            'x':d_x, 'y':2.03, 'z': z, # a gauche, à  1m50 de haut
            'cx':0., 'cy':d_y/2, 'cz': d_z/2, # on regarde le centre du plan de reference
            'foc': foc, 'pc_min': 0.01, 'pc_max': 10000  },
        ]
