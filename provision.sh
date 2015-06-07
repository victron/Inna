#!/usr/bin/env bash

# add multiverse
# add-apt-repository "deb http://archive.ubuntu.com/ubuntu trusty multiverse"
# add-apt-repository "deb-src http://archive.ubuntu.com/ubuntu trusty multiverse"
# add-apt-repository "deb http://archive.ubuntu.com/ubuntu trusty-updates multiverse"
# add-apt-repository "deb-src http://archive.ubuntu.com/ubuntu trusty-updates multiverse"

ln -sf /usr/share/zoneinfo/Europe/Kiev /etc/localtime

apt-get update
apt-get install -y python-setuptools
easy_install pip
apt-get install -y python-django
apt-get install -y sqlite3
apt-get install -y virtualenvwrapper
# apt-get install -y vsftpd

# pip install paramiko PyYAML Jinja2 httplib2

