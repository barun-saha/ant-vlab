#!/bin/sh
#
# Install several software required by the Software Engineering
# Virtual Lab.
#
# The package versions are specific to Ubuntu 12.04
# and may differ with other OS versions.
#
# Barun Saha (http://barunsaha.me)
# 18 March 2015, IIT Kharagpur
#

. ../scripts/common.sh

#APT_CONF_FILE=/etc/apt/apt.conf

#proxy=$(grep -i '^Acquire::http::proxy' $APT_CONF_FILE | cut -d' ' -f2 | tr -d '"' | tr -d ';')
#export http_proxy=$proxy
#export https_proxy=$proxy

#echo $http_proxy
#echo $https_proxy



MAX_ATTEMPTS=2
COUNTER=1
while [[ $COUNTER -le $MAX_ATTEMPTS ]]
do
	log 'Installing necessary Python packages'

	# Upgrade pip
	sudo -E pip install -U setuptools
	sudo -E pip install -U pip

	# Django version problem
	#sudo -E pip install Django==1.4.2
	sudo -E pip install Django==1.8.4

	# Environment error while installing 'MySQL-python' package
	# http://stackoverflow.com/questions/5178292/pip-install-mysql-python-fails-with-environmenterror-mysql-config-not-found
	sudo -E apt-get -y install libmysqlclient-dev
	sudo -E pip install MySQL-python

	# Commented because it autimatically updates the Django to the newest version
	#sudo -E pip install django-maintenancemode
	# sudo -E pip install django-ajaxcomments
	# sudo -E pip install django-tinymce
	# sudo -E pip install recaptcha-client
	sudo -E pip install PIL

	sudo -E pip install django-js-reverse
	
	sudo -E pip install rq
	sudo -E pip install django-rq

	sudo -E apt-get update

	COUNTER=$((COUNTER + 1))
done
