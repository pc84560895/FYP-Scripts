#!/bin/bash

#docker
wget -qO- https://get.docker.com/ | sh

#create a main directory
mkdir ~/HOSTTools
cd ~/HOSTTools

#create honeypot directory
#mkdir Honeypots
#cd Honeypots

#create database for filtered logs
#cp ~/FYP-Scripts/honeypotlogsdb.py .
#python honeypotlogsdb.py
#rm honeypotlogsdb.py

#Install MySQL-python
#pip install MySQL-python

# cowrie docker file
#docker pull ouspg/cowrie

# kippo docker file
#docker pull tomdesinto/kippo

#Install Requests
pip install requests

# Install splunk forwarder
wget "https://www.splunk.com/bin/splunk/DownloadActivityServlet?architecture=x86_64&platform=linux&version=6.6.2&product=universalforwarder&filename=splunkforwarder-6.6.2-4b804538c686-linux-2.6-amd64.deb&wget=true" -O splunkuf
dpkg -i splunkuf
rm -rf splunkuf
/opt/splunkforwarder/bin/splunk enable boot-start --accept-license
