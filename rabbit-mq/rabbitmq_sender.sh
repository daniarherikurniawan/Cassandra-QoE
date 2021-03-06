#!/bin/bash


for wkl in '90' '95' '100' '105' '110' '115' '120' '125' '130' '135'
do
    echo 'Start PRIORITY workload '$wkl'rps'
    python3 sender_async_tm.py 100000 0 $wkl >> senderfile_temp.txt
    echo 'Workload Complete!'
    sleep 30s
done

for wkl in '90' '95' '100' '105' '110' '115' '120' '125' '130' '135'
do
    echo 'Start FIFO workload '$wkl'rps'
    python3 sender_async_tm.py 100000 1 $wkl >> senderfile_temp.txt
    echo 'Workload Complete!'
    sleep 30s
done

rm senderfile_temp.txt
