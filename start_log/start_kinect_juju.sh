#!/bin/bash          
STR="Start Kinect Server!"
cd /home/biogene/Dropbox/TROPIQUE/pyTropique/acquisition/version1/server_kin/
for i in {1..5}
do
	echo "Welcome $i times"
	/home/biogene/Dropbox/TROPIQUE/pyTropique/acquisition/version1/server_kin/server_kin_0.py &
	childpid=$!
	echo "child pid of spawned command is $childpid"
	sleep 10
	echo "a kill kill"
	kill $childpid
	sleep 5
	/home/tropic/biogene/TROPIQUE/pyTropique/acquisition/version1/server_kin/server_kin_1.py &
	childpid=$!
	echo "child pid of spawned command is $childpid"
	sleep 10
	echo "a kill kill"
	kill $childpid
	sleep 5
done
/home/biogene/Dropbox/TROPIQUE/pyTropique/acquisition/version1/server_kin/server_kin_0.py &
childpid=$!
echo "child pid of spawned command is $childpid"
/home/biogene/Dropbox/TROPIQUE/pyTropique/acquisition/version1/server_kin/server_kin_1.py &
childpid=$!
echo "child pid of spawned command is $childpid"
echo "goodbye"



