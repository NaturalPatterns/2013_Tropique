#!/bin/bash          
STR="Start Kinect Server!"
cd /home/tropic/Dropbox/TROPIQUE/pyTropique/acquisition/version1/server_kin/
for i in {1..5}
do
	echo "Welcome $i times"
	/home/tropic/Dropbox/TROPIQUE/pyTropique/acquisition/version1/server_kin/server_kin_0.py &
	childpid=$!
	echo "child pid of spawned command is $childpid"
	sleep 10
	echo "a kill kill"
	kill $childpid
	sleep 5
	/home/tropic/Dropbox/TROPIQUE/pyTropique/acquisition/version1/server_kin/server_kin_1.py &
	childpid=$!
	echo "child pid of spawned command is $childpid"
	sleep 10
	echo "a kill kill"
	kill $childpid
	sleep 5
done
/home/tropic/Dropbox/TROPIQUE/pyTropique/acquisition/version1/server_kin/server_kin_0.py &
childpid=$!
echo "child pid of spawned command is $childpid"
/home/tropic/Dropbox/TROPIQUE/pyTropique/acquisition/version1/server_kin/server_kin_1.py &
childpid=$!
echo "child pid of spawned command is $childpid"
echo "goodbye"



