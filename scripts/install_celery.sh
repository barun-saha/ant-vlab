#!/bin/bash

# Packages

source ../scripts/common.sh

log ''
log '*** Executing install_celery.sh'


# Removing directories
sudo rm celery-2.3.3.tar.gz django-celery-2.3.2.tar.gz
sudo rm -rf celery-2.3.3 django-celery-2.3.2
echo 'Existing directories removed'

DOWNLOAD_URL_CELERY='https://pypi.python.org/packages/source/c/celery/celery-2.3.3.tar.gz'
DOWNLOAD_URL_DJCELERY='https://pypi.python.org/packages/source/d/django-celery/django-celery-2.3.2.tar.gz'

CURRENT_DIR=$(pwd)
HOME_PATH=/home/barun
ANT_PATH=$HOME_PATH/codes/www/vlabs

CELERY_DIR=celery-2.3.3/
DJCELERY_DIR=django-celery-2.3.2/
ETC_DEFAULT=/etc/default/
ETC_INIT_D=/etc/init.d/
CELERYD_LOC_DEFAULT=$CURRENT_DIR/conf/etc/default/celeryd
CELERYD_LOC_INIT_D=$CURRENT_DIR/conf/etc/init.d/celeryd

# Downloading celery and django-celery
wget -O celery-2.3.3.tar.gz "$DOWNLOAD_URL_CELERY"
wget -O django-celery-2.3.2.tar.gz "$DOWNLOAD_URL_DJCELERY"

# Installation celery
log 'Installing celery'
tar xvfz celery-2.3.3.tar.gz
cd "$CELERY_DIR"
python setup.py build
python setup.py install # as root
cd "$CURRENT_DIR"

# Installing django-celery
log 'Installing django-celery'
tar xvfz django-celery-2.3.2.tar.gz
cd "$DJCELERY_DIR"
python setup.py install
cd "$CURRENT_DIR"

# Copying celeryd
log 'Copying celeryd'
cp "$CELERYD_LOC_DEFAULT" "$ETC_DEFAULT"
cp "$CELERYD_LOC_INIT_D" "$ETC_INIT_D"

sudo update-rc.d celeryd defaults


# Avoiding prompt
#http://stackoverflow.com/questions/30540060/deleting-unused-models-stale-content-types-prompt
log 'Executing syncdb'
python $ANT_PATH/manage.py syncdb --noinput

if [[ $? -ne 0 ]]
then
    echo 'Failed to run syncdb!'
    error 'Failed to run syncdb!'
fi

#python $ANT_PATH/manage.py celeryd






