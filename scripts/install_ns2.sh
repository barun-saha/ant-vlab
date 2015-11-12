#!/bin/bash

# Download NS-2 and other packages from GitHub
# Since the file size is large, wget may fail. In that case we retry 
# upto 5 times.

DOWNLOAD_URL_NS='https://github.com/barun-saha/ns2-wimax-bluetooth-wsn/archive/master.zip'
DOWNLOAD_URL_TCL='http://sourceforge.net/projects/tcl/files/Tcl/8.4.19/tcl8.4.19-src.tar.gz/download'
DOWNLOAD_URL_TK='http://sourceforge.net/projects/tcl/files/Tcl/8.4.19/tk8.4.19-src.tar.gz/download'
DOWNLOAD_URL_OTCL='http://sourceforge.net/projects/otcl-tclcl/files/OTcl/1.13/otcl-src-1.13.tar.gz/download'
DOWNLOAD_URL_TCLCL='http://sourceforge.net/projects/otcl-tclcl/files/TclCL/1.19/tclcl-src-1.19.tar.gz/download'

# Removing directories
sudo rm master.zip tcl8.4.19-src.tar.gz tk8.4.19-src.tar.gz otcl-src-1.13.tar.gz tclcl-src-1.19.tar.gz
sudo rm -rf ns2-wimax-bluetooth-wsn-master tcl8.4.19 tk8.4.19 otcl-1.13 tclcl-1.19
echo 'Existing directories removed'

wget "$DOWNLOAD_URL_NS"
wget -O tcl8.4.19-src.tar.gz "$DOWNLOAD_URL_TCL"
wget -O tk8.4.19-src.tar.gz "$DOWNLOAD_URL_TK"
wget -O otcl-src-1.13.tar.gz "$DOWNLOAD_URL_OTCL"
wget -O tclcl-src-1.19.tar.gz "$DOWNLOAD_URL_TCLCL"
echo 'Download successful'

# Extract the zip file
unzip master
tar -xzf tcl8.4.19-src.tar.gz
tar -xzf tk8.4.19-src.tar.gz
tar -xzf otcl-src-1.13.tar.gz
tar -xzf tclcl-src-1.19.tar.gz
echo 'Unzip successful'

CURRENT_DIR=$(pwd)

# Path inside which `make` would be executed for each package
TCL_DIR=tcl8.4.19/unix/
TK_DIR=tk8.4.19/unix/
OTCL_DIR=otcl-1.13/
OTCL_LIB=$CURRENT_DIR/$OTCL_DIR
TCLCL_DIR=tclcl-1.19/
NS2_DIR=ns2-wimax-bluetooth-wsn-master/ns-2.34/
LIB_DIR=/usr/lib


# Error handling functions
cd_failed() {
	echo "Unable to change to location $1 (current location: $2)!"
	echo 'Aborting installation'
	exit 1
}

configure_failed() {
	echo "Configuration failed in $1"
	echo 'Aborting installation'
	exit 1
}

make_failed() {
	echo "Make failed in $1"
	echo 'Aborting installation'
	exit 1
}


# Install Tcl
echo 'Installing tcl'
cd "$TCL_DIR" || cd_failed "$TCL_DIR" "$CURRENT_DIR"
make clean
./configure || configure_failed "$TCL_DIR"
make || make_failed "$TCL_DIR"
sudo make install
cd "$CURRENT_DIR"

# Install Tk
echo 'Installing tk'
cd "$TK_DIR" || cd_failed "$TK_DIR" "$CURRENT_DIR"
make clean
./configure || configure_failed "$TK_DIR"
make || make_failed "$TK_DIR"
sudo make install
cd "$CURRENT_DIR"

# Install OTcl
echo 'Installing otcl'
cd "$OTCL_DIR" || cd_failed "$OTCL_DIR" "$CURRENT_DIR"
make clean
./configure --with-tcl=../tcl8.4.19 --with-tk=../tk8.4.19 || configure_failed "$OTCL_DIR"
make || make_failed "$OTCL_DIR"
sudo make install
cd "$CURRENT_DIR"

# Install Tclcl
echo 'Installing tclcl'
cd "$TCLCL_DIR" || cd_failed "$TCLCL_DIR" "$CURRENT_DIR"
make clean
./configure --with-tcl=../tcl8.4.19 --with-tk=../tk8.4.19 || configure_failed "$TCLCL_DIR"
make || make_failed "$TCLCL_DIR"
sudo make install
cd "$CURRENT_DIR"

# Creating symlinks to link the shared objects
echo 'Creating symlinks'
cd $LIB_DIR
sudo ln -s $CURRENT_DIR/$TCL_DIR/libtcl8.4.so libtcl8.4.so
sudo ln -s $CURRENT_DIR/$TK_DIR/libtk8.4.so libtk8.4.so
sudo ln -s $CURRENT_DIR/$OTCL_DIR/libotcl.so libotcl.so
cd "$CURRENT_DIR"


# Install NS-2
echo 'Installing ns-2'
cd "$NS2_DIR" || cd_failed "$NS2_DIR" "$CURRENT_DIR"

# Checking whether 64-bit system
# If 64-bit, then apply patch, otherwise skip patching
# Source: http://stackoverflow.com/a/21188486/147021

BIT_INFO=$(getconf LONG_BIT)
value=64

if [ $BIT_INFO = $value ]
then 
	#applying 64-bit.patch
	echo 'This is a 64-bit machine'
	echo 'Applying patch for 64-bit'
	cd ..
	patch -s -p1 < 64-bit.patch
	echo '64-bit patch applied'
	cd ..
	cd "$NS2_DIR" || cd_failed "$NS2_DIR" "$CURRENT_DIR"
fi

./configure --with-tcl=../../tcl8.4.19 --with-otcl=../../otcl-1.13 --with-tclcl=../../tclcl-1.19 || configure_failed "$NS2_DIR"
make clean
make || make_failed "$NS2_DIR"
sudo make install

echo 'NS-2 Installation successful'
