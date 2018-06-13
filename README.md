#Leva Api Development Guide

##For apache configuration

    sudo apt-get install libapache2-mod-wsgi-py3

##Development setup

##Install required system packages:

    sudo apt-get install python3-pip
    sudo apt-get install python3-dev python3-setuptools
    sudo apt-get install libpq-dev
    sudo apt-get install postgresql postgresql-contrib
    sudo apt-get install libmysqlclient-dev
    
    
##Create www directory where project sites and environment dir

    sudo mkdir /var/www && mkdir /var/envs && mkdir /var/envs/bin

##Install virtualenvwrapper

    sudo pip3 install virtualenvwrapper
    sudo pip3 install --upgrade virtualenv

##Add these to your bashrc virutualenvwrapper work

    export WORKON_HOME=/var/envs
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    export PROJECT_HOME=/var/www
    export VIRTUALENVWRAPPER_HOOK_DIR=/var/envs/bin    
    source /usr/local/bin/virtualenvwrapper.sh

##Create virtualenv

    cd /var/envs && mkvirtualenv --python=/usr/bin/python3 leva_api


##Install requirements for a project.

    cd /var/www/leva_api && pip install -r requirements/local.txt

    sudo chown :www-data /var/www/leva_api
    sudo cp /var/www/car/car/wsgi_default.py /var/www/leva_api/leva_api/wsgi.py


##Database creation
###For psql

    sudo su - postgres
    psql
    DROP DATABASE IF EXISTS leva;
    CREATE DATABASE leva;
    CREATE USER leva_user WITH password 'root';
    GRANT ALL privileges ON DATABASE leva TO leva_user;
    ALTER USER leva_user CREATEDB;



##Set up supervisor (pm2)

    $ sudo apt-get install python-software-properties
    $ curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
    $ sudo apt-get install nodejs
    $ cd /var/www/leva_api/
    $ pm2 startup ubuntu14
    $ pm2 start scripts/init_default_consumer.sh --name leva_api_init_default_consumer
    $ pm2 save



##Configure rabbitmq-server to run workers.
###/var/www/django_rest_apiAdd virtual host, and set permissions.

    $ sudo rabbitmqctl add_vhost leva
    $ sudo rabbitmqctl add_user leva_user root
    $ sudo rabbitmqctl set_permissions -p leva leva_user ".*" ".*" ".*"

