# Usage : ./fake.sh /Users/lup/Desktop/Tropique/fakenect/smoke_tunnel4 ./segmentation.py
#
# See documentation on http://brandynwhite.com/fakenect-openkinect-driver-simulator-experime
# Sensor Dumps
# http://dl.dropbox.com/u/15736519/thanksgiving0.tar.bz2
# http://dl.dropbox.com/u/15736519/legos0.tar.bz2
# http://dl.dropbox.com/u/15736519/sophie0.tar.bz2
#
# LD_PRELOAD="/usr/local/lib/fakenect/libfreenect.so" FAKENECT_PATH="../../build/utils/legos0" ./demo_cv_async.py
# 
# or on OS X
# 
#DYLD_LIBRARY_PATH="/usr/local/lib/fakenect/" FAKENECT_PATH="/Users/lup/Desktop/Tropique/fakenect/smoke_tunnel4" ./segmentation.py
DYLD_LIBRARY_PATH="/usr/local/lib/fakenect/" FAKENECT_PATH="$1" $2
