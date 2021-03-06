#!/bin/bash
echo 'This script will install the required dependencies to run Logger'

echo 'Installing MySQL'
sudo apt install mysql-server -y

echo 'Installing MySQLdb-python'
sudo apt-get install build-essential python-dev libmysqlclient-dev -y
sudo apt-get install python-mysqldb -y

echo 'Installing Matplotlib'
sudo apt-get install python-matplotlib -y

echo 'Installing pip'
sudo apt-get install python-pip -y

echo 'Installing pyprind'
sudo -H pip install pyprind

python setup.py
