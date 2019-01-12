#!/bin/bash

for wkl in '100' '120'
do
    echo 'Start workload '$wkl'rps'
    python3 sender_async_tm.py 100000 5000 $wkl >> senderfile_temp.txt
    echo 'Send Complete!'
    sleep 1m
done
