#!/bin/bash

#docker
wget -qO- https://get.docker.com/ | sh

#create a main directory
mkdir ~/HOSTTools
cd ~/HOSTTools

#create honeypot directory
mkdir honeypots
cd honeypots

#create database for filtered logs
cp ~/FYP-Scripts/honeypotlogsdb.py .
python honeypotlogsdb.py
rm honeypotlogsdb.py

# cowrie docker file
#docker pull ouspg/cowrie

# kippo docker file
#docker pull tomdesinto/kippo

