#!/bin/bash

-----------50K Msg Size------------
mkdir results

for wkl in '90' '120' '150' '180' '190' '200' '210' '220' '225' '230' '235' '240' '245' '250' '255' '260'
do
    echo 'Start listen workload '$wkl'rps'
    python3 receiver_tm.py > 'results/workload_'$wkl.txt
    sleep 2s
    echo 'Start listening to next workload .....'
done
zip -r results.zip results
echo 'All the things are finished'

------------------------------------
for wkl in '90' '120' '150' '180' '190' '200' '210' '220' '225' '230' '235' '240' '245' '250' '255' '260'
do
    echo 'Start workload '$wkl'rps'
    python sender_async_tm.py 50000 12000 $wkl >> senderfile_temp.txt
    echo 'Send Complete!'
    sleep 1m
done
rm senderfile_temp.txt

-----------50K Msg Size------------


------------200K Msg Size---------------


for wkl in '30' '35' '40' '45' '50' '55' '60' '65' '70'
do
    echo 'Start listen workload '$wkl'rps'
    python3 receiver_tm.py > 'results/workload_'$wkl.txt
    sleep 2s
    echo 'Start listening to next workload .....'
done
zip -r results.zip results
echo 'All the things are finished'




for wkl in '30' '35' '40' '45' '50' '55' '60' '65' '70'
do
    echo 'Start workload '$wkl'rps'
    python sender_async_tm.py 200000 3500 $wkl >> senderfile_temp.txt
    echo 'Send Complete!'
    sleep 1m
done
rm senderfile_temp.txt


------------200K Msg Size---------------


ONERF WORKLOAD

for wkl in '90' '95' '100' '105' '110' '115' '118' '119' '120'