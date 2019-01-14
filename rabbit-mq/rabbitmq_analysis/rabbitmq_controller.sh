#!/bin/bash

echo 'controller start working'
scp -r zhangbjb@pc344.emulab.net:/tmp/Cassandra-QoE/rabbit-mq/results_onerf_fifo ./
scp -r zhangbjb@pc344.emulab.net:/tmp/Cassandra-QoE/rabbit-mq/results_onerf_priority ./
mkdir rabbitmqdata
python3 fileprocessing.py
python3 RabbitMQV3.py
rm -r results_onerf_fifo
rm -r results_onerf_priority
rm -r rabbitmqdata
echo 'controller ends'
