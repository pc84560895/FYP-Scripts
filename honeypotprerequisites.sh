#!/bin/bash

#docker
wget -qO- https://get.docker.com/ | sh

#create a main directory
mkdir ~/HOSTTools
cd ~/HOSTTools

#Install Requests
pip install requests

# Install splunk forwarder
wget 'https://github.com/pc84560895/FYP-Scripts/blob/master/splunkuf.deb?raw=true' -O splunkuf.deb
dpkg -i splunkuf.deb
rm -rf splunkuf.deb
/opt/splunkforwarder/bin/splunk enable boot-start --accept-license --answer-yes
/opt/splunkforwarder/bin/splunk start --accept-license --answer-yes