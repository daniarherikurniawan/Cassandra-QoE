# rabbit.sh
# ubuntu 16.04
# https://www.rabbitmq.com/install-debian.html#apt

apt-key adv --keyserver "hkps.pool.sks-keyservers.net" --recv-keys "0x6B73A36E6026DFCA"

sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list <<EOF
deb https://dl.bintray.com/rabbitmq-erlang/debian xenial erlang
deb https://dl.bintray.com/rabbitmq/debian xenial main
EOF

sudo apt-get update

sudo apt-get install rabbitmq-server

sudo invoke-rc.d rabbitmq-server start
systemctl status rabbitmq-server.service

bash
pip install pika

python send.py

sudo rabbitmqctl list_queues


sudo invoke-rc.d rabbitmq-server stop