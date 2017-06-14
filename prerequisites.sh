#!/bin/bash

#docker
wget -qO- https://get.docker.com/ | sh

#create a main directory
mkdir ~/HOSTTools
cd HOSTTools

# masscan
git clone https://github.com/robertdavidgraham/masscan
cd masscan
make
make regress
mv bin/masscan /usr/bin

# nmap
apt-get install nmap -y

# create directory for docker images
cd ~/HOSTTools
mkdir dockerimages
cd dockerimages

# cowrie docker file
docker pull ouspg/cowrie

# kippo docker file
docker pull tomdesinto/kippo

