# Installation for Rapsberry Pi 3

## Setup Raspberry Pi

1. Get latest Raspbian Lite at <https://www.raspberrypi.org/downloads/raspbian/>
1. Write image into the SD card using steps from <https://www.raspberrypi.org/documentation/installation/installing-images/>
1. Install SD card into the raspi and boot
1. Using `sudo raspi-config` configure locale, keyboard, activate SSH server, hostname. Reboot when finished
1. If you are using wifi, setup using instruction at <https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md>
1. `sudo apt-get update && sudo apt-get upgrade`
1. `sudo apt-get -y install git`


## Setup neversleepeyes

1. `mkdir ~/dev && cd ~/dev`
1. `git clone https://github.com/gregsaun/neversleepeyes.git`
1. `cd neversleepeyes/install`
1. `chmod +x install.sh`
1. `sudo ./install.sh`