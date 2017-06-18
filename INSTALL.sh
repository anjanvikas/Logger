echo '\nThis script will install the required dependencies to run Logger\n\n\n'

echo '\n\nInstalling MySQL\n\n'
sudo apt install mysql-server

echo '\n\nInstalling MySQLdb-python\n\n'
sudo apt-get install build-essential python-dev libmysqlclient-dev
sudo apt-get install python-mysqldb

echo '\n\nInstalling Matplotlib\n\n'
sudo apt-get install python-matplotlib

python setup.py
