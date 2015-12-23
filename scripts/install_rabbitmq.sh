#!/bin/bash

source ../scripts/common.sh

log ''
log '*** Executing install_rabbitmq.sh'

# Moved to install_ubuntu_packages.sh

## Erlang dependencies installation
#sudo -E apt-get -y install build-essential libncurses5-dev openssl libssl-dev fop xsltproc unixodbc-dev
#sudo -E apt-get -y install --fix-missing


# Removing directories
sudo rm otp_src_R15B01.tar.gz
sudo rm -rf otp_src_R15B01
echo 'Existing directories removed'

DOWNLOAD_URL_ERLANG='http://erlang.org/download/otp_src_R15B01.tar.gz'

wget -O otp_src_R15B01.tar.gz "$DOWNLOAD_URL_ERLANG"

# unzip Erlang
tar zxvf otp_src_R15B01.tar.gz

CURRENT_DIR=$(pwd)
ERLANG_DIR=otp_src_R15B01/

# Install Erlang
log 'Installing Erlang'
cd "$ERLANG_DIR"
./configure
sudo make
sudo make install
cd "$CURRENT_DIR"

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
