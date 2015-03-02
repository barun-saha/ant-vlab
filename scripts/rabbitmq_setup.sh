#!/bin/sh

#
# Setup RabbitMQ
# Credentials are read from the rabbitmq_credentials.sh file. A dummy
# file is provided herein, but the values should be changed in a real
# setup. Contents of that file should be kept private.
#
# Barun Saha
# IIT Kharagpur
# 24 March 2014
#

# Read the user name, password and the host name
source rabbitmq_credentials.sh

rabbitmqctl add_user $R_USER_ID $R_PASSWORD
rabbitmqctl add_vhost $R_VHOST
rabbitmqctl set_permissions -p $R_VHOST $R_USER_ID ".*" ".*" ".*"
