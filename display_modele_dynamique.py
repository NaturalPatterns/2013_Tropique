#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Particle-like simulations using pyglet.app

Exploration mode.

    Interaction keyboard:
    - TAB pour passer/sortir du fulscreen
    - espace : passage en first-person persepective

    Les interactions visuo - sonores sont simulées ici par des switches lançant les événements:
    - R : rugosité G_struct distance_struct
    - P : pulse (modif de la longueur et raideur des segments)
    - V : G_repulsion <> G_repulsion_hot
    - G : G_rot <> G_rot_hot
    - Q : restore la config sans event
    - B : break
    - D : Down
    TODO: il reste de la place...

"""
# HACK; to avoid the "AccessInit: hash collision: 3 for both 1 and 1" bug...
# see http://forum.jetbrains.com/thread/PyCharm-938
import sys
import PIL.Image
sys.modules['Image'] = PIL.Image
# TODO: modele 3D blending fog / épaisseur du triangle / projection fond de la salle
# TODO: paramètre scan pour rechercher des bifurcations (edge of chaos)
# TODO: contrôle de la vitesse du mouvement de position simulé
########################################
#window = pyglet.window.Window(fullscreen='-fs' in sys.argv, config=config)
from parametres import VPs, volume, p, kinects_network_config, d_x, d_y, d_z, scenario, calibration
from modele_dynamique import Scenario
s = Scenario(p['N'], scenario, volume, VPs, p, calibration)
########################################
do_firstperson, foc_fp, i_VP_fp, alpha_fp, int_fp, intB_fp, show_VP = False, 60., 1, .1, 1., 0.01, True
s.heading_fp, s.rot_heading_fp, s.inc_heading_fp = 0., 0., 0.1
i_VP = 1  # VP utilisé comme projecteur en mode projection
do_fs = True  # fullscreen par défaut?
do_fs = False  # fullscreen par défaut?
do_slider = False
do_slider = True
do_sock=True
do_sock = False
########################################
i_win = 0
foc_VP = 50.
foc_VP = VPs[i_win]['foc']
########################################
if do_sock:
    sys.path.append('../network/')
    from network import Kinects
    k = Kinects(kinects_network_config)
else:
    positions = None

# Window information
# ------------------
import pyglet
#pyglet.options['darwin_cocoa'] = True
platform = pyglet.window.get_platform()
print "platform" , platform
display = platform.get_default_display()
print "display" , display
screens = display.get_screens()
print "screens" , screens
for i, screen in enumerate(screens):
    print 'Screen %d: %dx%d at (%d,%d)' % (i, screen.width, screen.height, screen.x, screen.y)
#screen   = screens[0]
N_screen = len(screens) # number of screens
N_screen = 1# len(screens) # number of screens
assert N_screen == 1 # we should be running on one screen only


from pyglet.window import Window
#from pyglet import clock

if do_fs:
    win_0 = Window(screen=screens[0], fullscreen=True, resizable=True)
else:
    win_0 = Window(width=screen.width*2/3, height=screen.height*2/3, screen=screens[0], fullscreen=False, resizable=True)
    win_0.set_location(screen.width/3, screen.height/3)

#print screen.width
import pyglet.gl as gl
fps_text = pyglet.clock.ClockDisplay()
from pyglet.gl.glu import gluLookAt
import numpy as np
def on_resize(width, height):
    gl.glViewport(0, 0, width, height)
    gl.glEnable(gl.GL_BLEND)
    gl.glShadeModel(gl.GL_SMOOTH) #
#     gl.glBlendFunc (gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
#     gl.glHint(gl.GL_LINE_SMOOTH, gl.GL_NICEST)# gl.GL_FASTEST)# gl.GL_NICEST)# GL_DONT_CARE)#
    gl.glDepthFunc(gl.GL_LEQUAL)
    gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT, gl.GL_NICEST)# gl.GL_FASTEST)# gl.GL_NICEST)# GL_DONT_CARE)#
    gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glDisable(gl.GL_LINE_SMOOTH)
    gl.glColor3f(1.0, 1.0, 1.0)
    gl.glDisable(gl.GL_CLIP_PLANE0)
    gl.glDisable(gl.GL_CLIP_PLANE1)
    gl.glDisable(gl.GL_CLIP_PLANE2)
    gl.glDisable(gl.GL_CLIP_PLANE3)
    return pyglet.event.EVENT_HANDLED

win_0.on_resize = on_resize
win_0.set_visible(True)
# win_0.set_mouse_visible(False)
gl.glMatrixMode(gl.GL_MODELVIEW)
gl.glLoadIdentity()
gl.gluPerspective(foc_VP, 1.0*win_0.width/win_0.height, VPs[i_win]['pc_min'], VPs[i_win]['pc_max'])
gluLookAt(VPs[i_win]['x'], VPs[i_win]['y'], VPs[i_win]['z'],
      VPs[i_win]['cx'], VPs[i_win]['cy'], VPs[i_win]['cz'],
      0., 0, 1.0)
#win_0.on_draw = on_draw
# batch = pyglet.graphics.Batch()

events = [0, 0, 0, 0, 0, 0, 0, 0] # 8 types d'événéments

@win_0.event
def on_key_press(symbol, modifiers):
    global events, do_firstperson, s
    if symbol == pyglet.window.key.TAB:
        if win_0.fullscreen:
            win_0.set_fullscreen(False)
            win_0.set_location(screen.width/3, screen.height/3)
        else:
            win_0.set_fullscreen(True)
    elif symbol == pyglet.window.key.SPACE:
        do_firstperson = not(do_firstperson)
    elif symbol == pyglet.window.key.LEFT:
        s.rot_heading_fp += s.inc_heading_fp
        # print s.rot_heading_fp
    elif symbol == pyglet.window.key.RIGHT:
        s.rot_heading_fp -= s.inc_heading_fp
        # print s.rot_heading_fp
    elif symbol == pyglet.window.key.B:
        events = [1, 1, 1, 1, 1, 1, 1, 0] # 8 types d'événéments
    elif symbol == pyglet.window.key.D:
        events = [0, 0, 0, 0, 0, 0, 0, 0] # 8 types d'événéments
    elif symbol == pyglet.window.key.R:
        events[0] = 1 - events[0]
    elif symbol == pyglet.window.key.P:
        events[1] = 1 - events[1]
    elif symbol == pyglet.window.key.V:
        events[2] = 1 - events[2]
    elif symbol == pyglet.window.key.G:
        events[4] = 1 - events[4]
    elif symbol == pyglet.window.key.S:
        events[7] = 1 - events[7]
    else:
        print symbol
    print events

from numpy import sin, cos, pi

@win_0.event
def on_resize(width, height):
    print 'The window was resized to %dx%d' % (width, height)
##if DEBUG: fps_display = pyglet.clock.ClockDisplay(color=(1., 1., 1., 1.))
@win_0.event
def on_draw():
    global s
    t = s.t

    if do_sock:
        positions = k.read_sock() # TODO: c'est bien une liste de coordonnées [x, y, z] ?
    else:
        # pour simuler ROGER:
        positions = []
        amp, amp2 = .2, .5
        T, T2 = 25., 30. # periode en secondes
        #positions.append([s.roger[0], s.roger[1], s.roger[2]]) #  bouge pas, roger.
        positions.append([s.roger[0] * (1. + amp*cos(2*pi*s.t/T2)), s.roger[1] * (1. + amp*cos(2*pi*s.t/T)), 1.*s.roger[2]]) # une autre personne dans un mouvement en phase
        positions.append([s.roger[0] * (1. + amp*sin(2*pi*s.t/T2)), s.roger[1] * (1. + amp*sin(2*pi*s.t/T)), 1.2*s.roger[2]]) # une autre personne dans un mouvement en phase
        positions.append([s.roger[0] * (1. + amp2*cos(2*pi*s.t/T2)), s.roger[1] * (1. + amp2*cos(2*pi*s.t/T)), 1.*s.roger[2]]) # une autre personne dans un mouvement en phase
        # positions.append([s.roger[0], s.roger[1] * (1. + amp2*cos(2*pi*s.t/T2)), 1.1*s.roger[2]]) # une personne dans un mouvement circulaire (elipse)


    s.do_scenario(positions=positions, events=events)

    win_0.clear()
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    if do_firstperson:
        gl.glEnable(gl.GL_FOG)
        gl.glFogi (gl.GL_FOG_MODE, gl.GL_LINEAR)
        # gl.glFogfv (gl.GL_FOG_COLOR, [0.8,0.8,0.8, 1.])
        gl.glHint (gl.GL_FOG_HINT, gl.GL_NICEST)#GL_DONT_CARE)
        gl.glFogf (gl.GL_FOG_DENSITY, 0.0000001)
        gl.glFogf (gl.GL_FOG_START, .0)
        gl.glFogf (gl.GL_FOG_END, 60.0)
        # gl.glClearColor(0.5, 0.5, 0.5, 1.0)

        gl.gluPerspective(foc_fp, 1.0*win_0.width/win_0.height,
                          VPs[i_VP_fp]['pc_min'], VPs[i_VP_fp]['pc_max'])
        x_fp, y_fp, z_fp = positions[0][0], positions[0][1], positions[0][2]
        s.heading_fp += s.rot_heading_fp * (s.t -t) # 2* pi * s.t / 30
        gluLookAt(x_fp, y_fp, z_fp,
                  x_fp + np.cos(s.heading_fp), y_fp + np.sin(s.heading_fp), z_fp,
                  0., 0, 1.0)
        # montre la salle comme un joli parallélipède bleu
        #gl.glPointSize(10)
        #gl.glColor3f(0., 0., 1.)
        #salle = [[0., 0., 0., d_x, 0., 0.], [0., 0., 0., 0., d_y, 0.], [0., 0., 0., 0., 0., d_z]]
        #pyglet.graphics.draw(2*3, gl.GL_LINES, ('v3f', salle))¬
        for VP in VPs:
            # marque la postion de chaque VP par un joli carré vert
            if show_VP:
                gl.glPointSize(10)
                gl.glColor3f(0., 1., 0.)
                pyglet.graphics.draw(1, gl.GL_POINTS, ('v3f', [VP['x'], VP['y'], VP['z']]))

            VP_ = np.array([[VP['x'], VP['y'], VP['z']]]).T * np.ones((1, s.N))
            p_ = s.particles[0:6, :].copy()
            # projecting the segment on the wall opposite to the VPs
            if VP['x'] > d_x/2: # un VP du coté x=0, on projete sur le plan x=0
                p_[1] = d_x / (d_x - p_[0]) * (p_[1]-VP['y']) + VP['y']
                p_[2] = d_x / (d_x - p_[0]) * (p_[2]-VP['z']) + VP['z']
                p_[4] = d_x / (d_x - p_[3]) * (p_[4]-VP['y']) + VP['y']
                p_[5] = d_x / (d_x - p_[3]) * (p_[5]-VP['z']) + VP['z']
                p_[0] = 0
                p_[3] = 0
            else:
                p_[1] = d_x / (p_[0]) * (p_[1]-VP['y']) + VP['y']
                p_[2] = d_x / (p_[0]) * (p_[2]-VP['z']) + VP['z']
                p_[4] = d_x / (p_[3]) * (p_[4]-VP['y']) + VP['y']
                p_[5] = d_x / (p_[3]) * (p_[5]-VP['z']) + VP['z']
                p_[0] = d_x
                p_[3] = d_x
            colors_ = np.array([int_fp, int_fp, int_fp, alpha_fp, intB_fp, intB_fp, intB_fp, alpha_fp, intB_fp, intB_fp, intB_fp, alpha_fp])[:, np.newaxis] * np.ones((1, s.N))
            pyglet.graphics.draw(3*s.N, gl.GL_TRIANGLES,
                                 ('v3f', np.vstack((VP_, p_)).T.ravel().tolist()),
                                 ('c4f', colors_.T.ravel().tolist()))

    else:
        gl.glDisable(gl.GL_FOG)
        gl.gluPerspective(foc_VP, 1.0*win_0.width/win_0.height,
                          VPs[i_VP]['pc_min'], VPs[i_VP]['pc_max'])
        gluLookAt(VPs[i_VP]['x'], VPs[i_VP]['y'], VPs[i_VP]['z'],
                  VPs[i_VP]['cx'], VPs[i_VP]['cy'], VPs[i_VP]['cz'],
                  0., 0, 1.0)

        # TODO: make an option to view particles from above
        #gl.gluOrtho2D(0.0, d_y, 0., d_z)

        gl.glLineWidth (p['line_width'])
        # marque la postion des personnes par un joli carré rouge
        for position in positions:
            gl.glPointSize(10)
            gl.glColor3f(1., 0., 0.)
            pyglet.graphics.draw(1, gl.GL_POINTS, ('v3f', position))

        gl.glColor3f(1., 1., 1.)

        pyglet.graphics.draw(2*s.N, gl.GL_LINES, ('v3f', s.particles[0:6, :].T.ravel().tolist()))
        #int_p, alpha_p = 1., 1. #.5 + .5*np.sin(2*np.pi*0.2 * s.t)
        #colors_ = np.array([int_p, int_p, int_p, alpha_p, int_p, int_p, int_p, alpha_p])[:, np.newaxis] * np.ones((1, s.N))
        #pyglet.graphics.draw(2*s.N, gl.GL_LINES, ('v3f', s.particles[0:6, :].T.ravel().tolist()),
                                 #('c4f', colors_.T.ravel().tolist()))


#    fps_text.draw()
#     batch.draw()


    if do_sock: k.trigger()

def callback(dt):
    global do_sock
    try :
        if DEBUG: print '%f seconds since last callback' % dt , '%f  fps' % pyglet.clock.get_fps()
    except :
        pass

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
        # f_manager.window.move(0, 0) dioes not work on MacOsX
        f_manager.set_window_title(" Quand c'est trop c'est tropicoooo ")

    #    AX = fig.add_subplot(111)
        plt.ion()
        # turn interactive mode on for dynamic updates.  If you aren't in interactive mode, you'll need to use a GUI event handler/timer.
        from matplotlib.widgets import Slider as slider_pylab
        ax, value = [], []
        n_key = len(p.keys())*1.
    #    print s.p.keys()
        liste_keys = p.keys()
        liste_keys.sort()
        for i_key, key in enumerate(liste_keys):
    #        print [0.1, 0.05+i_key/(n_key+1)*.9, 0.9, 0.05]
            ax.append(fig.add_axes([0.15, 0.05+i_key/(n_key-1)*.9, 0.6, 0.05], axisbg='lightgoldenrodyellow'))
            if p[key] > 0:
                value.append(slider_pylab(ax[i_key], key, 0., (p[key] + (p[key]==0)*1.)*10, valinit=p[key]))
            else:
                value.append(slider_pylab(ax[i_key], key,  (p[key] + (p[key]==0)*1.)*10,  -(p[key] + (p[key]==0)*1.)*10, valinit=p[key]))

        def update(val):
            for i_key, key in enumerate(liste_keys):
                p[key]= value[i_key].val
                print key, p[key]#, value[i_key].val
            plt.draw()

        for i_key, key in enumerate(liste_keys): value[i_key].on_changed(update)

        plt.show(block=False) # il faut pylab.ion() pour pas avoir de blocage

        return fig

    if s.scenario=='leapfrog' and do_slider:
        fig = sliders(s.p)
except Exception, e:
    print('problem while importing sliders ! Error = ', e)

pyglet.clock.schedule(callback)
pyglet.app.run()
print 'Goodbye'
