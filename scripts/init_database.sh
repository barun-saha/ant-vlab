#!/bin/bash
#
# This script creates the MySQL database, a user ID and password, and provides
# privileges to the user on the tables of the database. The contents would be
# inserted into the tables of the database created.
#
# Source: http://clubmate.fi/shell-script-to-create-mysql-database/
#
# Barun Saha (http://barunsaha.me)
# 11 March 2015, IIT Kharagpur
#

# The root password for MySQL database is shared by both SE and ANT in case
# they are hosted in the same container.
# HOME_PATH and ANT_PATH are inherited from the invoking script (configure.sh).

source ../scripts/common.sh

log ''
log '*** Executing init_database.sh'
log $TIMESTAMP 'Host: ' $SYSTEM
log 'Current directory is: ' $CURRENT_DIR
log 'Proxy is: ' $PROXY

HOME_PATH=/home/barun
ANT_DB_ROOT_PASSWD_FILE=$HOME_PATH/ant_mysql_root_passwd
ANT_DB_USR_PASSWD_FILE=$HOME_PATH/ant_mysql_usr_passwd
DUMP_FILE=$HOME_PATH/content/cse28-ant_db.sql
DB=db_isad
USR=u_isad

ROOT_PASSWD=x
USR_PASSWD=x
# Max no. of times MySQL installation would be attempted
MAX_ATTEMPTS=5

# If the root password file exists, read the root password
# Otherwise, create the file
log 'Reading password for MySQL root user'

if [[ -f "$ANT_DB_ROOT_PASSWD_FILE" && -r "$ANT_DB_ROOT_PASSWD_FILE" ]]
then
    ROOT_PASSWD=$(cat "$ANT_DB_ROOT_PASSWD_FILE")
else
    ROOT_PASSWD=$(generate_password)
    echo "$ROOT_PASSWD" > "$ANT_DB_ROOT_PASSWD_FILE"
    chmod -w "$ANT_DB_ROOT_PASSWD_FILE"
fi


log 'Reading password for MySQL user'

if [[ -f "$ANT_DB_USR_PASSWD_FILE" && -r "$ANT_DB_USR_PASSWD_FILE" ]]
then
    USR_PASSWD=$(cat "$ANT_DB_USR_PASSWD_FILE")
else
    USR_PASSWD=$(generate_password)
    echo "$USR_PASSWD" > "$ANT_DB_USR_PASSWD_FILE"
    chmod -w "$ANT_DB_USR_PASSWD_FILE"

    # Since the MySQL user's password is generated again, it is possible that
    # credentials.py used by Django contains an old database password. So,
    # remove that file to better be safe.
    rm -f "$ANT_PATH/credentials.py"
fi


## Database installation
sudo -E apt-get -y install debconf debconf-utils
# For purging debconf settings
echo PURGE | debconf-communicate mysql-server

log 'Installing MySQL'
sudo DEBIAN_FRONTEND=noninteractive apt-get remove --purge -y "^mysql.*"
#sudo apt-get autoremove
#sudo apt-get autoclean
sudo rm -rf /var/lib/mysql
sudo rm -rf /var/log/mysql 

#ROOT_PASSWD=$(cat "$ROOT_PASSWD")
echo mysql-server mysql-server/root_password password $ROOT_PASSWD | debconf-set-selections
echo mysql-server mysql-server/root_password_again password $ROOT_PASSWD | debconf-set-selections

counter=1
while [[ $counter -le $MAX_ATTEMPTS ]]
do
    sudo -E DEBIAN_FRONTEND=noninteractive apt-get -y install mysql-server
    sudo -E apt-get install --fix-missing
    
    if [[ $? -eq 0 ]]
    then
        log 'mysql-server installed!'
        break
    else
        if [[ $counter -eq $MAX_ATTEMPTS ]]
        then
            error 'Installation of mysql-server failed!'
        fi
    fi

    counter=$((counter + 1))
done


## Database creation
# SQL
Q1="CREATE DATABASE IF NOT EXISTS $DB;"
Q2="GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, REFERENCES, INDEX, ALTER, LOCK TABLES ON \`$DB\`.* TO '$USR'@'localhost' IDENTIFIED BY '$USR_PASSWD';"
Q3="FLUSH PRIVILEGES;"

SQL="${Q1}${Q2}${Q3}"

log 'Creating database'
MYSQL=$(which mysql)
log "mysql location is $MYSQL"
$MYSQL --user=root --password=$ROOT_PASSWD --execute="$SQL"

if [[ $? -ne 0 ]]
then
    error 'Failed to create MySQL database!'
fi

log "Database $DB created."


# Now initialize the databse with contents
log 'Restoring database dump'
$MYSQL --user=root --password=$ROOT_PASSWD "$DB" < "$DUMP_FILE"

if [[ $? -ne 0 ]]
then
    error 'Failed to initialize database with SQL dump!'
fi


# Managed in makefile

## Invoke syncdb to create tables necessary for Django -- but has Django been
## installed yet?
#log '11. Executing syncdb'
#PYTHON=$(which python)
#$PYTHON $SE_PATH/manage.py syncdb

#if [[ $? -ne 0 ]]
#then
#    error 'Failed to run syncdb!'
#fi
