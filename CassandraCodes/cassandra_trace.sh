#!/usr/bin/env bash

mkdir results_cass_scan
for ((t=20; t<=80; t++))
do
    python3 cassandraclient.py $t
    mv cass_read_latency.txt 'results_cass_scan/cass_read_latency_'$t.txt
done
echo 'Collection is OK'
zip -r results_cass_scan.zip results_cass_scan

