#!/bin/bash

#docker
wget -qO- https://get.docker.com/ | sh

#create a main directory
mkdir ~/HOSTTools
cd ~/HOSTTools

# cowrie docker file
docker pull ouspg/cowrie

# kippo docker file
docker pull tomdesinto/kippo

