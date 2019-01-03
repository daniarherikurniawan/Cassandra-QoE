#!/bin/bash

for wkl in '90' '120' '150' '180' '190' '200' '210' '220' '225' '230' '235' '240' '245' '250' '255' '260'
do
    echo 'Start workload '$wkl'rps'
    python sender_async_tm.py 50000 6000 $wkl >> senderfile_temp.txt
    echo 'Send Complete!'
    sleep 1m
done
rm senderfile_temp.txt