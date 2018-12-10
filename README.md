# Cassandra-QoE

chmod 777 up.sh

git add --all .
git commit -m "minor update" -a
git push origin master

There are 3 Cassandra nodes:
- cass-1.cassandra-qoe.cs331-uc.emulab.net
- cass-2.cassandra-qoe.cs331-uc.emulab.net
- cass-3.cassandra-qoe.cs331-uc.emulab.net

====================================================================================
> Install Java8

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

> run in cass-3

	cd /tmp/
	git clone https://github.com/daniarherikurniawan/Cassandra-QoE.git
	cd /tmp/Cassandra-QoE/apache-cassandra-3.0.17
	cp conf/cassandra3.yaml conf/cassandra.yaml 
	cd bin
	sudo chmod 777 cassandra
	cd /tmp/Cassandra-QoE/apache-cassandra-3.0.17/bin/
	./cassandra -f

> run in client

	cd /tmp/
	git clone https://github.com/daniarherikurniawan/Cassandra-QoE.git
	cd /tmp/Cassandra-QoE/apache-cassandra-3.0.17
	sudo apt-get update
	printf 'Y' | sudo apt-get install python-pip
	pip -V
	export LC_ALL=C
	pip install cassandra-driver
	pip install Faker

	python


====================================================================================
> open a new ssh on any node to check the status of Cassandra cluster

	cd /tmp/Cassandra-QoE/apache-cassandra-3.0.17/bin
	sudo chmod 777 nodetool
	./nodetool status


====================================================================================
<!-- csh -->
> preparation for running cqlsh
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
> Insert dataset from CSV
	
	./cqlsh $myIP
	USE CassDB;

	COPY CassDB.users (id,name,address,salary,phone) FROM '../../dataset/data-users-1.csv' WITH DELIMITER='|' AND HEADER=TRUE;

====================================================================================
> Another Query

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













