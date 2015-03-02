#!/bin/sh

# User account required for hosting the source code
# Note: The default user is barun -- if you change this, you need to
# manually update the settings.py file
USER=barun
useradd -m "$USER"

HOME_PATH=/home/"$USER"
ANT_PATH=$HOME_PATH/codes/www/vlabs
CUR_PATH=$(pwd)
# Path where the source of NS-3 is present
NS3_PATH=/home/barun/Desktop/ns3/ns-allinone-3.10/ns-3.10

# Directories where intermediate files would be created
mkdir -p /var/vlabs/ant/ns3
chown -R www-data /var/vlabs

#mv ../codes /home/barun/codes
mv ../codes "$HOME_PATH"/codes
cp ../conf/httpd.conf /etc/apache2/
mv ../conf/www /usr/local/
mv ../etc /etc
mv ../_wimax_ref_ /var/vlabs/ant


# TODO: Copy celery files (celery should be installed before this)


# Initialize the database
# Note: You must have the following two SQL files available
mysql -u root < cse28-ant_init.sql
mysql -u root db_ant < cse28-ant_db.sql

# Create symlinks
ln -s /var/vlabs/ "$ANT_PATH"/media/vlabs
ln -s /var/vlabs/ant/vlabs /var/vlabs
ln -s /var/vlabs/ant/ns3/ $NS3_PATH/ns3ant

# Generate the secret key
cd "$ANT_PATH" && python utils/generate_secret_key.py
cd "$CUR_PATH"


# For RabbitMQ (RabbitMQ should be installed before this)
cd "$ANT_PATH" && python manage.py syncdb


# TODO: Install celery and django-celery


# TODO: Install NS-2


# TODO: Install NS-3


# TODO: Execute permissions.py to change group for NS-3 installation
# and provide write permission to the group. Refer to
# https://github.com/barun-saha/ns3_vlab
