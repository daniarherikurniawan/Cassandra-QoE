#!/bin/bash

for wkl in '90' '95' '100' '105' '110' '115' '120'
do
    echo 'Start FIFO workload '$wkl'rps'
    python3 sender_async_tm.py 100000 1 $wkl >> senderfile_temp.txt
    echo 'Send Complete!'
    sleep 1m
done

for wkl in '90' '95' '100' '105' '110' '115' '120'
do
    echo 'Start PRIORITY workload '$wkl'rps'
    python3 sender_async_tm.py 100000 0 $wkl >> senderfile_temp.txt
    echo 'Send Complete!'
    sleep 1m
done

rm senderfile_temp.txt
