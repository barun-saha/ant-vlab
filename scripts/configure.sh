#!/bin/sh

source ../scripts/common.sh

log ''
log '*** Executing configure.sh'
log $TIMESTAMP 'Host: ' $SYSTEM
log 'Current directory is: ' $CURRENT_DIR


# User account required for hosting the source code
# Note: The default user is barun -- if you change this, you need to
# manually update the settings.py file


create_user() {
	log 'Creating user barun'
	useradd -m "$1"
}


USER=barun
# Check if user exists
id $USER > /dev/null 2>&1
[[ $? -eq 0 ]] && log "User $USER exists" || \
                  create_user "$USER"


CUR_PATH=$(pwd)

export HOME_PATH=/home/"$USER"
export ANT_PATH=$HOME_PATH/codes/www/vlabs
APACHE_DEFAULT_FILE=/etc/apache2/sites-available/default
APACHE_DEFAULT_SSL_FILE=/etc/apache2/sites-available/default-ssl

# Directories where intermediate files would be created
log 'Creating directories'
mkdir -p /var/vlabs/ant/ns3
chown -R www-data /var/vlabs

# Copying Apache configuration files
log ' 3. Copying Apache configuration file'
echo '' > /etc/apache2/httpd.conf

# Remove the default configuration files
[ -f "$APACHE_DEFAULT_FILE" ] && rm "$APACHE_DEFAULT_FILE"
[ -f "$APACHE_DEFAULT_SSL_FILE" ] && rm "$APACHE_DEFAULT_SSL_FILE"
cp conf/default "$APACHE_DEFAULT_FILE"

apache2ctl restart
