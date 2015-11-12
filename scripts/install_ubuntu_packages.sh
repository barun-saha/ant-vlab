#!/bin/sh
#
# Install several software required by the Advanced Network Technologies
# Virtual Lab.
#
# The package versions are specific to Ubuntu 12.04
# and may differ with other OS versions.
#
# Barun Saha (http://barunsaha.me)
# 18 March 2015, IIT Kharagpur
#

source ../scripts/common.sh

log 'Installing necessary Ubuntu packages'

# Installation of individual packages for NS2

sudo -E apt-get -y install build-essential
sudo -E apt-get -y install --fix-missing
sudo -E apt-get -y install pkg-config
sudo -E apt-get -y install --fix-missing
sudo -E apt-get -y install automake bison flex
sudo -E apt-get -y install --fix-missing
sudo -E apt-get -y install make makedev
sudo -E apt-get -y install --fix-missing
sudo -E apt-get -y install g++ g++-4.4 gcc gcc-4.4 gcc-4.4-base gccxml
sudo -E apt-get -y install --fix-missing
sudo -E apt-get -y install libx11-6 libx11-data libx11-dev libxmu-dev libxmu-headers libxmu6 libxmuu-dev libxmuu1
sudo -E apt-get -y install --fix-missing
#sudo apt-get -y install libboost-python-dev libboost-python1.40-dev libboost-python1.40.0 libgcc1 libgv-python
#sudo -E apt-get -y install --fix-missing
