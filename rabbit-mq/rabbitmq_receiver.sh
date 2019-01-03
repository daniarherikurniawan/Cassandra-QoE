#!/bin/bash

mkdir results

for wkl in '90' '120' '150' '180' '190' '200' '210' '220' '225' '230' '235' '240' '245' '250' '255' '260'
do
    echo 'Start listen workload '$wkl'rps'
    python3 receiver_tm.py > 'results/workload_'$wkl.txt
    sleep 2s
    echo 'Start listening to next workload .....'
done
zip results.zip results