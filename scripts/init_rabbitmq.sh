#!/bin/bash

source ../scripts/rabbitmq_credentials.sh
source ../scripts/common.sh

log ''
log '*** Executing init_rabbitmq.sh'
log $TIMESTAMP 'Host: ' $SYSTEM
log 'Current directory is: ' $CURRENT_DIR
log 'Proxy is: ' $PROXY

HOME_PATH=/home/barun
ANT_RMQ_USR_PASSWD_FILE=$HOME_PATH/ant_rmq_usr_passwd

log 'Reading password for RabbitMQ user'

if [[ -f "$ANT_RMQ_USR_PASSWD_FILE" && -r "$ANT_RMQ_USR_PASSWD_FILE" ]]
then
    USR_PASSWD=$(cat "$ANT_RMQ_USR_PASSWD_FILE")
else
    USR_PASSWD=$(generate_password)
    echo "$USR_PASSWD" > "$ANT_RMQ_USR_PASSWD_FILE"
    chmod -w "$ANT_RMQ_USR_PASSWD_FILE"
fi

log 'Setting RabbitMQ user, vhost, and permissions'

sudo rabbitmqctl add_user $R_USER_ID $USR_PASSWD
sudo rabbitmqctl add_vhost $R_VHOST
sudo rabbitmqctl set_permissions -p $R_VHOST $R_USER_ID ".*" ".*" ".*"
