#!/bin/bash

source ../scripts/common.sh

log ''
log '*** Executing install_rabbitmq.sh'
log $TIMESTAMP 'Host: ' $SYSTEM
log 'Current directory is: ' $CURRENT_DIR
log 'Proxy is: ' $PROXY


# Install Erlang
log 'Installing Erlang'
echo 'deb http://packages.erlang-solutions.com/ubuntu precise contrib' >> /etc/apt/sources.list
wget -O erlang-signing-key-public.asc http://packages.erlang-solutions.com/ubuntu/erlang_solutions.asc
sudo apt-key add erlang-signing-key-public.asc
sudo rm -rf /var/lib/apt/lists/*
sudo apt-get update
sudo apt-get install erlang
sudo apt-get install erlang-nox


# Install RabbitMQ
log 'Installing RabbitMQ'
echo "deb http://www.rabbitmq.com/debian/ testing main"  | sudo tee  /etc/apt/sources.list.d/rabbitmq.list > /dev/null
wget -O rabbitmq-signing-key-public.asc https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
sudo apt-key add rabbitmq-signing-key-public.asc
sudo rm -rf /var/lib/apt/lists/*


# Max no. of times rabbitmq-server installation would be attempted
MAX_ATTEMPTS=5
counter=1
while [[ $counter -le $MAX_ATTEMPTS ]]
do
    sudo -E apt-get update
    sudo -E apt-get install rabbitmq-server -y
    sudo -E apt-get install --fix-missing
    
    if [[ $? -eq 0 ]]
    then
        log 'rabbitmq-server installed!'
        break
    else
        if [[ $counter -eq $MAX_ATTEMPTS ]]
        then
            error 'Installation of rabbitmq-server failed!'
        fi
    fi

    counter=$((counter + 1))
done


sudo service rabbitmq-server start
sudo rabbitmq-plugins enable rabbitmq_management
sudo service rabbitmq-server restart

# Initializing RabbitMQ
log 'Invoking script to initialize RabbitMQ'
bash ../scripts/init_rabbitmq.sh
