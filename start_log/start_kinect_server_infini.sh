#!/bin/bash
STR="Start Kinect Server!"
cd /home/tropic/Dropbox/TROPIQUE/pyTropique/acquisition/
for i in {1..5}
do
	echo "Welcome $i times"
	/home/tropic/Dropbox/TROPIQUE/pyTropique/acquisition/server_kinect.py 0 0 &
	childpid=$!
	echo "child pid of spawned command is $childpid"
	sleep 10
	echo "a kill kill"
	kill $childpid
	sleep 5
	/home/tropic/Dropbox/TROPIQUE/pyTropique/acquisition/server_kinect.py 1 0 &
	childpid=$!
	echo "child pid of spawned command is $childpid"
	sleep 10
	echo "a kill kill"
	kill $childpid
	sleep 5
done
/home/tropic/Dropbox/TROPIQUE/pyTropique/acquisition/server_kinect.py 0 0 &
childpid=$!
echo "child pid of spawned command is $childpid"
/home/tropic/Dropbox/TROPIQUE/pyTropique/acquisition/server_kinect.py 1 0 &
childpid=$!
echo "child pid of spawned command is $childpid"
echo "goodbye"



