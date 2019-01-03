#!/bin/bash

mkdir results

for wkl in '30' '35' '40' '45' '50' '55' '60' '65' '70'
do
    echo 'Start listen workload '$wkl'rps'
    python3 receiver_tm.py > 'results/workload_'$wkl.txt
    sleep 2s
    echo 'Start listening to next workload .....'
done
zip -r results.zip results
echo 'All the things are finished'