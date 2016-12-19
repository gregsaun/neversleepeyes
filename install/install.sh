#!/bin/bash

sudo apt-get update

# Packages for gphoto2 and libgphoto2 from normal repository
#apt-get -y install python-pip python-dev gphoto2 libgphoto2-2-dev

# Prepare installation of latest tarball release of gphoto2 and libgphoto2
gp_version="2.5.11"
sudo apt-get -y install libexif-dev libltdl-dev libpopt-dev libaa1-dev libjpeg8-dev libcdk5-dev
wget -0 libgphoto2-${gp_version}.tar.gz https://sourceforge.net/projects/gphoto/files/libgphoto/${gp_version}/libgphoto2-${gp_version}.tar.gz/download
wget -0 gphoto2-${gp_version}.tar.gz    https://sourceforge.net/projects/gphoto/files/gphoto/${gp_version}/gphoto2-${gp_version}.tar.gz/download
tar -xvf libgphoto2-${gp_version}.tar.gz
tar -xvf gphoto2-${gp_version}.tar.gz

# Install libgphoto2
cd libgphoto2-${gp_version}/
./configure
make
sudo make install

# Install gphoto2
cd ../gphoto2-${gp_version}/
./configure
make
sudo make install

# Check gphoto2 install
echo "\n\n====================================="
echo "Version installed :"
gphoto2 --version | tail -3
if [ $(gphoto2 --version | tail -3 | awk '/^gphoto2/ {print $2}') != "${gp_version}" ]; then
	echo "ERROR: wrong version of gphoto2, should be ${gp_version}"
	exit -1
fi
if [ $(gphoto2 --version | tail -3 | awk '/^libgphoto2/ {print $2}') != "${gp_version}" ]; then
	echo "ERROR: wrong version of libgphoto2, should be ${gp_version}"
	exit -1
fi
echo "====================================="

# Clean up
cd ../
rm -rf libgphoto2-${gp_version}.tar.gz gphoto2-${gp_version}.tar.gz libgphoto2-${gp_version} gphoto2-${gp_version}

# Installation of python-gphoto2 (python binding for libgphoto2)
# and other python modules
sudo apt-get -y install python-pip python-dev
pip install -r requirements.txt