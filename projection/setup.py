"""
Setup.py script for SimpleCellDemo, see http://www.incm.cnrs-mrs.fr/LaurentPerrinet/SimpleCellDemo


Usage:
    python setup.py py2app --iconfile=icon.icns

Prerequisites:
	pip install -u  py2app 


    http://svn.pythonmac.org/py2app/py2app/trunk/doc/index.html
"""

from setuptools import setup

NAME = 'interference' # 'gray-scott' #
APP = [NAME + '.py']
DATA_FILES = []
plist = dict(
    CFBundleIconFile            = 'icon.icns',
    CFBundleName                = NAME,
    CFBundleShortVersionString  = "0.1.0",
    CFBundleGetInfoString       = NAME,
    CFBundleExecutable          = NAME,
#     CFBundleIdentifier          = 'org.livingcode.examples.%s' % ID,
    NSHumanReadableCopyright    = 'Copyright 2011 Laurent Perrinet http://www.incm.cnrs-mrs.fr/LaurentPerrinet',
)

INCLUDES = ['ctypes.util', 'glumpy',]
# PACKAGES = [] /usr/local/lib/python2.7/site-packages/glumpy/image/filter.vert

OPTIONS = {
            'argv_emulation': False,
            'optimize':False,
            'site_packages':True,
#            'frameworks':['/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/PyAudio-0.2.3-py2.6-macosx-10.6-x86_64.egg/_portaudio.so', '/opt/local/lib/libcxcore.2.1.dylib', '/opt/local/lib/libcv.2.1.dylib', '/opt/local/lib/libcvaux.2.1.dylib', '/opt/local/lib/libhighgui.2.1.dylib', ], #'/usr/lib/libcam_iface_mega.dylib', '/usr/lib/libcam_iface_mega.0.dylib', '/usr/lib/libcam_iface_mega.0.5.9.dylib', '/Library/Frameworks/Python.framework/Versions/6.2/lib/python2.6/site-packages/_portaudio.so', 
# #             'packages': PACKAGES,
             'includes':INCLUDES,
            'plist':plist}

setup(
    app=APP,
    data_files=DATA_FILES,
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        'glumpy.image': ['*.vert', '*.frag'],
    },
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)



