#!/bin/bash

for wkl in '80' '90' '100' '105' '110' '115' '120' '125' '126' '127' '128' '129' '130'
do
    echo 'Start workload '$wkl'rps'
    python sender_async_tm.py 100000 4500 $wkl >> senderfile_temp.txt
    echo 'Send Complete!'
    sleep 1m
done
rm senderfile_temp.txt