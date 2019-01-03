#!/bin/bash

for wkl in '30' '35' '40' '45' '50' '55' '60' '65' '70'
do
    echo 'Start workload '$wkl'rps'
    python sender_async_tm.py 200000 2000 $wkl >> senderfile_temp.txt
    echo 'Send Complete!'
    sleep 1m
done
rm senderfile_temp.txt