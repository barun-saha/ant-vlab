#!/bin/bash

# Creating new user barun
USER_ID=barun
sudo useradd -m -s /bin/bash "$USER_ID"
##* Only used for testing -- should be disabled later
#echo $USER_ID:abcd | chpasswd
##* Takes effect in the next login
#sudo adduser $USER_ID sudo
##*

HOME_PATH=/home/$USER_ID
DESKTOP_PATH=/home/$USER_ID/Desktop
DOWNLOAD_URL_NS3='https://github.com/barun-saha/ns3_vlab/archive/master.zip'
BIN_PATH=/usr/bin
NS3_PATH=/home/$USER_ID/Desktop/ns3/ns-allinone-3.10


echo 'Home path created:' $HOME_PATH

sudo mkdir $DESKTOP_PATH
echo 'Desktop created'

## Creating NS_3 Directory
#mkdir ns3
#export NS3_PATH=/home/"$USER_ID"/Desktop/ns3

cd $DESKTOP_PATH
echo 'We are in:'
pwd

# Downloading NS3 from Github
#wget "$DOWNLOAD_URL_NS3"
sudo rm -rf ns3_vlab-master

# unzip master
unzip master

# Renaming the existing folder name ns3_vlab to ns3
sudo mv ns3_vlab-master ns3

# Going to /usr/bin folder
cd $BIN_PATH

# Creating symlink for gcc-4.4
sudo rm gcc
sudo ln -s gcc-4.4 gcc

# Creating symlink for g++-4.4
sudo rm g++
sudo ln -s g++-4.4 g++

# Creating synlink for ns3ant
cd $NS3_PATH/ns-3.10
sudo mkdir ns3ant
sudo ln -s /var/vlabs/ant/ns3 ns3ant

# Cleaning .waf file
cd $NS3_PATH/ns-3.10
./waf clean

build_failed() {
	echo "Build failed in $1"
	echo 'Aborting installation'
	exit 1
}

test_failed() {
	echo "Test failed in $1"
	echo 'Aborting installation'
	exit 1
}


# NS3 building
cd $NS3_PATH 
python build.py || build_failed "$NS3_PATH "
echo 'NS3 bulidling successful'

# Testing NS3 file
cd $NS3_PATH/ns-3.10
python test.py || test_failed "$NS3_PATH"
echo 'NS3 testing successful'

echo 'NS3 shell sript is running successfully'
