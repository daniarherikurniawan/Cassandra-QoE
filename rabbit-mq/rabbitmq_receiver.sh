#!/bin/bash

echo 'Start Priority Training Workload'
mkdir results_onerf_priority
for wkl in  '90' '95' '100' '105' '110' '115' '120' '125' '130' '135'
do
    echo 'Start listen workload '$wkl'rps'
    python3 receiver_tm.py > 'results_onerf_priority/workload_'$wkl.txt
    sleep 2s
    echo 'Start listening to next workload .....'
done
zip -r results_onerf_priority.zip results_onerf_priority


echo 'Start FIFO Training Workload'
mkdir results_onerf_fifo
for wkl in '90' '95' '100' '105' '110' '115' '120' '125' '130' '135'
do
    echo 'Start listen workload '$wkl'rps'
    python3 receiver_tm.py > 'results_onerf_fifo/workload_'$wkl.txt
    sleep 2s
    echo 'Start listening to next workload .....'
done
zip -r results_onerf_fifo.zip results_onerf_fifo

echo 'Start Analyzing Data'

ssh zhangbjb@pc725.emulab.net  > /dev/null 2>&1 << EOF
cd /tmp/Cassandra-QoE/rabbit-mq/rabbitmq_analysis
sh rabbitmq_controller.sh
exit
EOF

scp zhangbjb@pc725.emulab.net:/tmp/Cassandra-QoE/rabbit-mq/rabbitmq_analysis/final_results.txt ./
echo 'All EXP Finish, results are in final_results.txt'

