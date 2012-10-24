#!/bin/bash          
STR="Hello World!"
echo $STR
./server_kin_0.py &
childpid=$!
echo "child pid of spawned command is $childpid"
sleep 15
echo "a kill kill"
kill $childpid
echo "yeah kill"
sleep 5
echo "yeah reboot"
sleep 5
#shutdown -r now



