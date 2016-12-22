#!/bin/bash
################################################################################
#
# Description:
# Bash script to install all necessary tools
#
# Author: Gregoire Saunier
# Website: www.ekunn.com
# Creation date: 2016.12.22
#
# Resources:
#   - http://www.gphoto.org
#   - https://github.com/gphoto/
#   - https://github.com/gonzalo/gphoto2-updater
#   - https://github.com/jim-easterbrook/python-gphoto2
#
################################################################################


GP_VERSION="2.5.11"      # Version of gphoto2 release on github to install
LIBGP_VERSION="2.5.11.1" # Version of libgphoto2 used only to check installation


function log {
    echo -e "\n\n"
    echo "====================================="
    echo "${1}"
    echo "====================================="    
}


function raise_error {
    echo "ERROR: ${1}"
    exit -1
}


# Install gphoto2 and libgphoto2 from github sources
log "Install gphoto using gphoto2-updater"
wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh && 
chmod +x gphoto2-updater.sh && sudo ./gphoto2-updater.sh -d $GP_VERSION


# Check gphoto2 install
log "Check installation"
gphoto2 --version > /dev/null
if [ $? -ne 0 ]; then
        raise_error "gphoto2 doesn't seems to be installed correctly!"
fi
gphoto2 --version | tail -3
if [ $(gphoto2 --version | tail -3 | awk '/^gphoto2 / {print $2}') != "${GP_VERSION}" ]; then
        raise_error "wrong version of gphoto2, should be ${GP_VERSION}"
fi
if [ $(gphoto2 --version | tail -3 | awk '/^libgphoto2 / {print $2}') != "${LIBGP_VERSION}" ]; then
        raise_error "wrong version of libgphoto2, should be ${LIBGP_VERSION}"
fi
echo "gphoto2 and libgphoto2 are correctly installed :)"


# Installation of python-gphoto2 (python binding for libgphoto2)
# and other python modules
log "Install python tools"
sudo apt-get update && sudo apt-get -y install python-pip python-dev
sudo -H pip install -U pip
sudo -H pip install -r requirements.txt
python -c "import gphoto2 as gp; gp.check_result(gp.gp_context_new())"
if [ $? -ne 0 ]; then
        raise_error "python-gphoto2 doesn't seems to be installed correctly!"
fi

log "End of installation"