# une liste des kinects donnant leur adresse, port, position (x; y; z) et azimuth. le paramètre fake permet de lancer un client de  simulation plutot que la vraie segmentation 
kinects = [
        {'address':127.0.0.1, 'port': 50031, 'x':10.0, 'y':5.0, 'z': 4.3, 'az':-45, 'fake':True},
        {'address':127.0.0.1, 'port': 50032, 'x':10.0, 'y':5.0, 'z': 4.3, 'az':0 , 'fake':True}
        {'address':127.0.0.1, 'port': 50033, 'x':10.0, 'y':5.0, 'z': 4.3, 'az':45, 'fake':True },
        ]

# une liste des video projs donnant leur adresse, port, position (x; y; z) et azimuth. le paramètre fake permet de lancer un client de  simulation plutot que la vraie projection 

VPs = [
        {'address':127.0.0.1, 'port': 50034, 'x':10.0, 'y':5.0, 'z': 4.3, 'az':-45},
        {'address':127.0.0.1, 'port': 50035, 'x':10.0, 'y':5.0, 'z': 4.3, 'az':0 }
        {'address':127.0.0.1, 'port': 50036, 'x':10.0, 'y':5.0, 'z': 4.3, 'az':45 },
        ]
