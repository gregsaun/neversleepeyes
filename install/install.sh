#!/bin/bash

function raise_error {
	echo "ERROR: ${1}"
	exit -1
}

# Packages for gphoto2 and libgphoto2 from normal repository
#apt-get -y install python-pip python-dev gphoto2 libgphoto2-2-dev

# Prepare installation of latest tarball release of gphoto2 and libgphoto2
gp_version="2.5.11"
echo "====================================="
echo "Install lib for gphoto2 ${gp_version}"
echo "====================================="
sudo apt-get update
sudo apt-get -y install libexif-dev libltdl-dev libtool libpopt-dev libaa1-dev libjpeg8-dev libcdk5-dev build-essential libudev-dev pkg-config gettext #automake autoconf autopoint
wget -O libgphoto2-${gp_version}.tar.gz https://sourceforge.net/projects/gphoto/files/libgphoto/${gp_version}/libgphoto2-${gp_version}.tar.gz/download
wget -O gphoto2-${gp_version}.tar.gz    https://sourceforge.net/projects/gphoto/files/gphoto/${gp_version}/gphoto2-${gp_version}.tar.gz/download


# Install libgphoto2
echo -e "\n\n"
echo "====================================="
echo "Start libgphoto2 installation"
echo "====================================="
tar -xvf libgphoto2-${gp_version}.tar.gz
cd libgphoto2-${gp_version}/
./configure && make && sudo make install
if [ $? -ne 0 ]; then
	raise_error "something went wrong during installation of libgphoto2!"
fi
echo "====================================="
echo "End of libgphoto2 installation"
echo "====================================="


# Install gphoto2
echo -e "\n\n"
echo "====================================="
echo "Start gphoto2 installation"
echo "====================================="
tar -xvf gphoto2-${gp_version}.tar.gz
cd ../gphoto2-${gp_version}/
./configure && make && sudo make install
if [ $? -ne 0 ]; then
	raise_error "something went wrong during installation of gphoto2!"
fi
echo "====================================="
echo "End of gphoto2 installation"
echo "====================================="


# Check gphoto2 install
echo -e "\n\n"
echo "====================================="
echo "Version installed :"
gphoto2 --version > /dev/null
if [ $? -ne 0 ]; then
	raise_error "gphoto2 doesn't seems to be installed correctly!"
fi
gphoto2 --version | tail -3
if [ $(gphoto2 --version | tail -3 | awk '/^gphoto2 / {print $2}') != "${gp_version}" ]; then
	raise_error "wrong version of gphoto2, should be ${gp_version}"
fi
if [ $(gphoto2 --version | tail -3 | awk '/^libgphoto2 / {print $2}') != "${gp_version}" ]; then
	raise_error "wrong version of libgphoto2, should be ${gp_version}"
fi
echo "====================================="


# Clean up
cd ../
rm -rf libgphoto2-${gp_version}.tar.gz gphoto2-${gp_version}.tar.gz libgphoto2-${gp_version} gphoto2-${gp_version}


# Installation of python-gphoto2 (python binding for libgphoto2)
# and other python modules
echo -e "\n\n"
echo "====================================="
echo "Install python tools"
echo "====================================="
sudo apt-get -y install python-pip python-dev
sudo pip install -r requirements.txt
