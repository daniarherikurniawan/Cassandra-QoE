#!/bin/bash

mkdir results
for prio in '10' '9'
do
    for wkl in '10' '50'
    do
        echo 'testhaha' > 'results/prio_'$prio'_workload_'$wkl.txt
    done

done