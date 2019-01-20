#!/usr/bin/env bash

mkdir results
for ((t=40; t<=65; t++))
do
    python3 cassandraclient.py $t
    mv cass_read_latency.txt 'results/cass_read_latency_'$t.txt
done
echo 'Collection is OK'
zip -r results_cass_scan.zip results

