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
	cd Cassandra-QoE/apache-cassandra-3.0.17
	cp conf/cassandra1.yaml conf/cassandra.yaml 
	cd bin
	sudo chmod 777 cassandra
	cd /tmp/Cassandra-QoE/apache-cassandra-3.0.17/bin/
	./cassandra -f

> run in cass-2

	cd /tmp/
	git clone https://github.com/daniarherikurniawan/Cassandra-QoE.git
	cd Cassandra-QoE/apache-cassandra-3.0.17
	cp conf/cassandra2.yaml conf/cassandra.yaml 
	cd bin
	sudo chmod 777 cassandra
	cd /tmp/Cassandra-QoE/apache-cassandra-3.0.17/bin/
	./cassandra -f

> run in cass-3

	cd /tmp/
	git clone https://github.com/daniarherikurniawan/Cassandra-QoE.git
	cd Cassandra-QoE/apache-cassandra-3.0.17
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
> preparation for running cqlsh
#csh

	bash
	cd /tmp/Cassandra-QoE/
	chmod 777 scripts/getIP.sh
	myIP="$(./scripts/getIP.sh)"
	cd /tmp/Cassandra-QoE/apache-cassandra-3.0.17/bin
	chmod 777 cqlsh
	./cqlsh $myIP

====================================================================================
> Prepare the data and insert test data

	CREATE KEYSPACE test
		WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};

	USE test

	CREATE TABLE emp(
	   emp_id int PRIMARY KEY,
	   emp_name text,
	   emp_city text,
	   emp_sal varint,
	   emp_phone varint
	   );

	select * from emp;

	INSERT INTO emp (emp_id, emp_name, emp_city,
	   emp_phone, emp_sal) VALUES(1,'ram', 'Hyderabad', 9848022338, 50000);

	INSERT INTO emp (emp_id, emp_name, emp_city,
	   emp_phone, emp_sal) VALUES(2,'robin', 'Hyderabad', 9848022339, 40000);

	INSERT INTO emp (emp_id, emp_name, emp_city,
	   emp_phone, emp_sal) VALUES(3,'rahman', 'Chennai', 9848022330, 45000);

	select * from emp;


====================================================================================
> Another Query

	UPDATE emp SET emp_city='Delhi',emp_sal=50000
	   WHERE emp_id=2;

	SELECT emp_name, emp_sal from emp;

	CREATE INDEX ON emp(emp_sal);
	SELECT * FROM emp WHERE emp_sal=50000;

	DELETE FROM emp WHERE emp_id=3;

	exit

====================================================================================
> Insert test data using python driver

	printf 'Y' | sudo apt-get install python-pip
	pip -V
	export LC_ALL=C
	pip install cassandra-driver

	cd /tmp/Cassandra-QoE/
	python scripts/insertData.py














