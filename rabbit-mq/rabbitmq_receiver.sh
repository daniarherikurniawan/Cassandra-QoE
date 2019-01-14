#!/bin/bash

echo 'Start Priority workload'
mkdir results_onerf_priority
for wkl in '90' '95' '100' '105' '110' '115' '120'
do
    echo 'Start listen workload '$wkl'rps'
    python3 receiver_tm.py > 'results_onerf_priority/workload_'$wkl.txt
    sleep 2s
    echo 'Start listening to next workload .....'
done
zip -r results_onerf_priority.zip results_onerf_priority


echo 'Start FIFO workload'
mkdir results_onerf_fifo
for wkl in '90' '95' '100' '105' '110' '115' '120'
do
    echo 'Start listen workload '$wkl'rps'
    python3 receiver_tm.py > 'results_onerf_fifo/workload_'$wkl.txt
    sleep 2s
    echo 'Start listening to next workload .....'
done
zip -r results_onerf_fifo.zip results_onerf_fifo


echo 'Start Analyzing Data'
