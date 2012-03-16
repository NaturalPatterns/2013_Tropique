
#!/usr/bin/env python
# -*- coding: utf8 -*-


# une liste des kinects donnant leur adresse, port, position (x; y; z) et azimuth. le parametre fake permet de lancer un client de  simulation plutot que la vraie segmentation 
kinects = [
		{'address':'192.168.1.103', 'port': 9999, 'x':10.0, 'y':5.0, 'z': 4.3, 'az':-45, 'fake':True},
		{'address':'192.168.1.168', 'port': 9999, 'x':10.0, 'y':5.0, 'z': 4.3, 'az':0 , 'fake':True}		
		]

# une liste des video projs donnant leur adresse, port, position (x; y; z) et azimuth. le parametre fake permet de lancer un client de  simulation plutot que la vraie projection 
"""
VPs = [
        {'address':127.0.0.1, 'port': 50034, 'x':10.0, 'y':5.0, 'z': 4.3, 'az':-45},
        {'address':127.0.0.1, 'port': 50035, 'x':10.0, 'y':5.0, 'z': 4.3, 'az':0 },
        {'address':127.0.0.1, 'port': 50036, 'x':10.0, 'y':5.0, 'z': 4.3, 'az':45 }
        ]
"""
