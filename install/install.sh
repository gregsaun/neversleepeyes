#!/bin/bash

# Check if run as root
if [ "$EUID" -ne 0 ]
  then echo "Please run this script as root"
  exit
fi

apt-get update
apt-get -y install python-pip python-dev gphoto2 libgphoto2-2-dev
pip install -r requirements.txt