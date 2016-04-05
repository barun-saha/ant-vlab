#!/bin/sh

source ../scripts/common.sh

log ''
log '*** Executing deploy.sh'
log $TIMESTAMP 'Host: ' $SYSTEM
log 'Current directory is: ' $CURRENT_DIR

HOME_PATH=/home/barun
ANT_PATH=$HOME_PATH/codes/www/vlabs
APACHE_DEFAULT_FILE=/etc/apache2/sites-available/default
APACHE_DEFAULT_SSL_FILE=/etc/apache2/sites-available/default-ssl

# Moving codes and configuration files
log "Moving codes to $HOME_PATH/codes"
mkdir -p $HOME_PATH/codes
cp -r codes/* $HOME_PATH/codes/

# log "Moving other configuration files"
# cp -r conf/www /usr/local/
cp -r _wimax_ref_ /var/vlabs/ant

# Creating symlinks
log "Creating symlinks"
ln -sf /var/vlabs $ANT_PATH/media/vlabs
ln -sf /usr/bin/gcc-4.4 /usr/bin/gcc
ln -sf /usr/bin/g++-4.4 /usr/bin/g++

# Copying Apache configuration files
log 'Copying Apache configuration file'
echo '' > /etc/apache2/httpd.conf

# Remove the default configuration files
[ -f "$APACHE_DEFAULT_FILE" ] && rm "$APACHE_DEFAULT_FILE"
[ -f "$APACHE_DEFAULT_SSL_FILE" ] && rm "$APACHE_DEFAULT_SSL_FILE"
cp conf/default "$APACHE_DEFAULT_FILE"

log 'Restarting apache'
apache2ctl restart

log 'Collecting static files'
python $ANT_PATH/manage.py collectstatic --noinput
log 'Generating django_js_reverse.js'
python $ANT_PATH/manage.py collectstatic_js_reverse
# Symlink from static_media to access trace files
ln -s /var/vlabs/ant $ANT_PATH/static_media/traces
# Set ownership of files
chown -R barun:www-data $HOME_PATH/codes
# Apache needs write permission on vlabs/ to generate two files
chmod g+w $ANT_PATH
