### Checkout to branch `cass-read-from-local`
```
git checkout cass-read-from-local
```

### Compiling cassandra
This is optional, this repository already has compiled classes in `build` folder. You can run cassandra without recompile the source code.
```
cd cassandra
ant
```

### Config: Read from local only
Read from local only feature is turned off by default. To run read request in coordinator replica only, you have to add this following line in `conf/cassandra.yaml` :
```
read_from_local_only: true
```

### Client request
Python cassandra driver from datastax has load balancer by default. You have to override the default policy. This is the example

```python
# whitelist host should be IP address, if it is an url it won't work.
whitelist_host = ['127.0.0.1']
def is_address_accepted(host):
	return host.address in whitelist_host

filter_policy = HostFilterPolicy(
    child_policy=RoundRobinPolicy(),
    predicate=is_address_accepted
)

primary_host = ['127.0.0.1'];
cluster = Cluster(
    primary_host,
    load_balancing_policy=filter_policy,
)

session = cluster.connect()
```

### Run simple workload
Before run the workload you have to initialize the data. See [readme](README.md).
Run simple workload by:
```
python3 scripts/simple_request.py
```
