#!/bin/bash

mkdir results

for wkl in '90' '95' '100' '105' '110' '115' '120'
do
    echo 'Start listen workload '$wkl'rps'
    python3 receiver_tm.py > 'results/workload_'$wkl.txt
    sleep 2s
    echo 'Start listening to next workload .....'
done
zip -r results.zip results
echo 'All the things are finished'