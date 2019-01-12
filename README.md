# Cassandra-QoE

chmod 777 up.sh

git add --all .
git commit -m "minor update" -a
git push origin master

There is a front-end clients queue manager
- client.cassandra-qoe.DeepEdgeVideo.emulab.net

There is a replica selector
- selector.cassandra-qoe.DeepEdgeVideo.emulab.net

There are 3 Cassandra nodes:
- cass-1.cassandra-qoe.DeepEdgeVideo.emulab.net
- cass-2.cassandra-qoe.DeepEdgeVideo.emulab.net
- cass-3.cassandra-qoe.DeepEdgeVideo.emulab.net

Open 8 SSH terminal :
- 2 cass-1 (for inserting the CSV data and running cassandra)
- 1 cass-2 (for running cassandra)
- 1 cass-3 (for running cassandra)
- 1 selector (for waiting a request that will ask a replica address)
- 3 client (for sending rabbit-mq request, receiving rabbit-mq request, and asking the replica address to Selector)


====================================================================================
> Open SSH to all nodes
> Install Java8 on cassandra nodes

	sudo apt-get update
	printf "Y" | sudo apt-get install software-properties-common
	printf "\n" | sudo add-apt-repository ppa:webupd8team/java
	sudo apt-get update
	sudo apt-get install oracle-java8-set-default

====================================================================================
>run in cass-1

	cd /tmp/
	git clone https://github.com/daniarherikurniawan/Cassandra-QoE.git
	cd /tmp/Cassandra-QoE/apache-cassandra-3.0.17
	cp conf/cassandra1.yaml conf/cassandra.yaml 
	cd bin
	sudo chmod 777 cassandra
	cd /tmp/Cassandra-QoE/apache-cassandra-3.0.17/bin/
	./cassandra -f

> run in cass-2

	cd /tmp/
	git clone https://github.com/daniarherikurniawan/Cassandra-QoE.git
	cd /tmp/Cassandra-QoE/apache-cassandra-3.0.17
	cp conf/cassandra2.yaml conf/cassandra.yaml 
	cd bin
	sudo chmod 777 cassandra
	cd /tmp/Cassandra-QoE/apache-cassandra-3.0.17/bin/
	./cassandra -f

> run in cass-3 (run this after running cass-1 and cass-2)

	cd /tmp/
	git clone https://github.com/daniarherikurniawan/Cassandra-QoE.git
	cd /tmp/Cassandra-QoE/apache-cassandra-3.0.17
	cp conf/cassandra3.yaml conf/cassandra.yaml 
	cd bin
	sudo chmod 777 cassandra
	cd /tmp/Cassandra-QoE/apache-cassandra-3.0.17/bin/
	./cassandra -f

====================================================================================
> open a new ssh on any node to check the status of Cassandra cluster

	cd /tmp/Cassandra-QoE/apache-cassandra-3.0.17/bin
	sudo chmod 777 nodetool
	./nodetool status


====================================================================================
<!-- csh -->
> preparation for running cqlsh on any cassandra node
	
	#csh
	bash
	cd /tmp/Cassandra-QoE/
	chmod 777 scripts/*
	myIP="$(./scripts/getIP.sh)"
	echo $myIP
	cd /tmp/Cassandra-QoE/apache-cassandra-3.0.17/bin
	chmod 777 cqlsh
	./cqlsh $myIP


====================================================================================
> Prepare the data and insert test data

	CREATE KEYSPACE CassDB
		WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};

	USE CassDB;

	CREATE TABLE users(
	   id UUID PRIMARY KEY,
	   name text,
	   address text,
	   salary int,
	   phone text
	   );

	select * from users;

	INSERT INTO users (id, name, address,
	   salary, phone) VALUES(now(),'ram', 'Hyderabad', 50000, '9848022338');

	INSERT INTO users (id, name, address,
	   salary, phone) VALUES(now(),'robin', 'Hyderabad', 40000, '9848022339');

	INSERT INTO users (id, name, address,
	   salary, phone) VALUES(now(),'rahman', 'Chennai', 45000, '9848022330');

	select * from users;


====================================================================================
> Modify data payload of each item
  
    cd /tmp/Cassandra-QoE/dataset/
    python3 addpayload.py
> Insert dataset from CSV
	
	./cqlsh $myIP
	USE CassDB;

	COPY CassDB.users (id,name,address,salary,phone) FROM '../../dataset/data-users-1.csv' WITH DELIMITER='|' AND HEADER=TRUE;
	
	COPY CassDB.users (id,name,address,salary,phone) FROM '../../dataset/data-users-2.csv' WITH DELIMITER='|' AND HEADER=TRUE;
	COPY CassDB.users (id,name,address,salary,phone) FROM '../../dataset/data-users-3.csv' WITH DELIMITER='|' AND HEADER=TRUE;
	COPY CassDB.users (id,name,address,salary,phone) FROM '../../dataset/data-users-4.csv' WITH DELIMITER='|' AND HEADER=TRUE;
	COPY CassDB.users (id,name,address,salary,phone) FROM '../../dataset/data-users-5.csv' WITH DELIMITER='|' AND HEADER=TRUE;
	COPY CassDB.users (id,name,address,salary,phone) FROM '../../dataset/data-users-6.csv' WITH DELIMITER='|' AND HEADER=TRUE;
	COPY CassDB.users (id,name,address,salary,phone) FROM '../../dataset/data-users-7.csv' WITH DELIMITER='|' AND HEADER=TRUE;
	COPY CassDB.users (id,name,address,salary,phone) FROM '../../dataset/data-users-8.csv' WITH DELIMITER='|' AND HEADER=TRUE;
	COPY CassDB.users (id,name,address,salary,phone) FROM '../../dataset/data-users-9.csv' WITH DELIMITER='|' AND HEADER=TRUE;
	COPY CassDB.users (id,name,address,salary,phone) FROM '../../dataset/data-users-10.csv' WITH DELIMITER='|' AND HEADER=TRUE;

	
	


====================================================================================
> run in server (selector)
	
	cd /tmp/
	git clone https://github.com/daniarherikurniawan/Cassandra-QoE.git
	cd /tmp/Cassandra-QoE/
	python replica-selector/server.py

> run in client for rabbitMQ
	
	apt-key adv --keyserver "hkps.pool.sks-keyservers.net" --recv-keys "0x6B73A36E6026DFCA"

	sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list <<EOF
	deb https://dl.bintray.com/rabbitmq-erlang/debian xenial erlang
	deb https://dl.bintray.com/rabbitmq/debian xenial main
	EOF

	sudo apt-get update
	sudo apt-get install rabbitmq-server

	<!-- =================== -->
	// check the status of rabbitMQ, it should be automatically started

	sudo invoke-rc.d rabbitmq-server start
	systemctl status rabbitmq-server.service

	<!-- =================== -->
	// run rabbit-mq receiver
	
	python /tmp/Cassandra-QoE/rabbit-mq/receive.py


> run in client for preparing sending request 

	cd /tmp/
	git clone https://github.com/daniarherikurniawan/Cassandra-QoE.git
	cd /tmp/Cassandra-QoE/
	sudo apt-get update
 
	bash
	export LC_ALL=C

	sudo apt-get install python3-pip
	pip3 install cassandra-driver
	pip3 install Faker

	pip3 install pandas
	pip3 install matplotlib
	pip3 install datetime

	cd /tmp/Cassandra-QoE/dataset
	python3

	// run rabbit-mq sender

	python /tmp/Cassandra-QoE/rabbit-mq/send.py


> Make sure these files are running
- replica-selector/server.py (selector)
- rabbit-mq/receive.py (client)
- rabbit-mq/send.py (client)

> Note:
> You just need to edit the send.py and the algorithm at server.py

====================================================================================
> Python script for preparing the library

	import pandas as pd
	import io
	import matplotlib.pyplot as plt
	import numpy as np
	import datetime
	from datetime import timedelta
	from datetime import datetime

> Python script for getting the random uuid
	



====================================================================================
> Another Query
	
	./cqlsh $myIP
	USE CassDB;

	UPDATE users SET address='Delhi',salary=50000
	   WHERE id=e9454d00-fc01-11e8-add1-35de7ed92caa;

	SELECT name, salary from users;

	CREATE INDEX ON users(salary);
	SELECT * FROM users WHERE salary=50000;

	DELETE FROM users WHERE id=3e9454d00-fc01-11e8-add1-35de7ed92caa;

	SELECT * FROM users WHERE salary>1000 ALLOW FILTERING;

	DROP TABLE users;
	TRUNCATE CassDB.users;
	DESCRIBE TABLES;

	SELECT * FROM users LIMIT 10;

	SELECT COUNT(*) FROM users;

	CONSISTENCY

	exit

====================================================================================
> Insert test data using python driver

	sudo apt-get update
	printf 'Y' | sudo apt-get install python-pip
	pip -V
	export LC_ALL=C
	pip install cassandra-driver
	pip install Faker

	cd /tmp/Cassandra-QoE/
	python scripts/generateTestData.py


> Random
	
	// reduce .git size
	git reflog expire --all --expire=now
	git gc --prune=now --aggressive
	
=======================================================================
>Cpu/Memory/Space monitor
    
    sudo apt-get update
    sudo apt-get install sysstat
    top
    iostat
    mpstat
    
======================================================================
>YCSB Usage
    
    cd /tmp
    curl -O --location https://github.com/brianfrankcooper/YCSB/releases/download/0.15.0/ycsb-0.15.0.tar.gz
    tar xfvz ycsb-0.15.0.tar.gz
    cd ycsb-0.15.0
    
>Create YCSB Tables
    
    create keyspace ycsb with replication = {'class':'SimpleStrategy', 'replication_factor':1};
    use ycsb;
    create table usertable (y_id varchar primary key,field0 varchar,field1 varchar,field2 varchar,field3 varchar,field4 varchar,field5 varchar,field6 varchar,field7 varchar,field8 varchar,field9 varchar);
    
>Create Database from client
    
    ./bin/ycsb run cassandra-cql -P workloads/workloadb-test -p hosts=IP -threads 10
    
>Run workload from client

    ./bin/ycsb load cassandra-cql -P workloads/workloadb-test -p hosts=IP -threads 10

>Clear Old database

    use ycsb;
    truncate usetable;

>Delete Snapshots

>Ubuntu Script to Bash

    sudo dpkg-reconfigure dash  
    
    
    
==========================================================================================================
>Install RabbitMQ
	
	apt-key adv --keyserver "hkps.pool.sks-keyservers.net" --recv-keys "0x6B73A36E6026DFCA"

	sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list <<EOF
	deb https://dl.bintray.com/rabbitmq-erlang/debian xenial erlang
	deb https://dl.bintray.com/rabbitmq/debian xenial main
	EOF

	sudo apt-get update
	sudo apt-get install rabbitmq-server
	
>Install Pika & Numpy

	sudo apt-get update
	sudo apt-get install python3-pip
	pip3 install pika
	pip3 install numpy
	
>Start & Stop & Reset RabbitMQ service
	
	sudo invoke-rc.d rabbitmq-server start
	sudo invoke-rc.d rabbitmq-server stop
	sudo invoke-rc.d rabbitmq-server restart
	
>Set users

	sudo rabbitmqctl add_user test1 test1
	sudo rabbitmqctl set_user_tags test1 administrator
	sudo rabbitmqctl set_permissions -p / test1 ".*" ".*" ".*"
	
>Reset all things

	sudo rabbitmqctl stop
	sudo rabbitmqctl reset
	
>Clear logs

	sudo rabbitmqctl rotate_logs
    
>Sync Internet Time (ops.emulab.net)

	sudo ntpdate -u 155.98.33.74
	

=========================================================================================
>Copy file to windows system

	sudo apt-get install lrzsz
	sz <filename>












