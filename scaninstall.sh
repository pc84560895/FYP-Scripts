#!/bin/bash
apt-get --assume-yes install git gcc make libpcap-dev
mkdir temporary
cd temporary
git clone https://github.com/robertdavidgraham/masscan
cd masscan
make -j
make regress
mv bin/masscan /usr/bin/
apt-get --assume-yes install nmap
