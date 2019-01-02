#!/bin/bash

for prio in '10' '9' '8' '7' '6' '5' '4' '3' '2' '1'
do
    for wkl in '10' '50' '60' '90' '120' '150' '180' '210' '220' '225' '230' '235' '240' '245' '250' '255' '260'
    do
        echo 'Start priority '$prio' workload '$wkl
        python 50000 15000 $wkl $prio >> senderfile_temp.txt
        echo 'Send Complete!'
        sleep 1m
    done
done
rm senderfile_temp.txt