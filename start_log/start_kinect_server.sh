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
childpiddeun=$!
echo "child pid of childpiddeun command is $childpiddeun"
/home/tropic/Dropbox/TROPIQUE/pyTropique/acquisition/server_kinect.py 1 0 &
childpiddedeux=$!
echo "child pid of childpiddedeux command is $childpiddedeux"
echo "premiere partie fini"

while :
do
    sleep 1800
    echo "infinite loops [ hit CTRL+C to stop]"
    if ps -p $childpiddeun > /dev/null
        then
            echo "$childpiddeun childpiddeun is running"
        else
            echo "$childpiddeun childpiddeun is dead"
            /home/tropic/Dropbox/TROPIQUE/pyTropique/acquisition/server_kinect.py 0 0 &
            childpiddeun=$!
            sleep 60
    fi
    if ps -p $childpiddedeux > /dev/null
        then
            echo "$childpiddedeux childpiddedeux is running"
        else 
            echo "$childpiddedeux childpiddedeux is dead"
            /home/tropic/Dropbox/TROPIQUE/pyTropique/acquisition/server_kinect.py 1 0 &
            childpiddedeux=$!
            sleep 60
# Do something knowing the pid exists, i.e. the process with $PID is running
    fi
done



