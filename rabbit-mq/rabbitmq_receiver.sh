#!/bin/bash

mkdir results
for prio in '10' '9' '8' '7' '6' '5' '4' '3' '2' '1'
do
    for wkl in '10' '50' '60' '90' '120' '150' '180' '210' '220' '225' '230' '235' '240' '245' '250' '255' '260'
    do
        echo 'Start listen priority $prio workload $wkl'
        python3 receiver_tm.py > 'results/prio_'$prio'_workload_'$wkl.txt
        sleep 2s
        echo 'Start Next!'
    done
done
