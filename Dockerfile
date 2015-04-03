FROM ubuntu:latest

MAINTAINER Tige Phillips <tige@tigelane.com>

RUN apt-get update
RUN apt-get -y upgrade


############
# APACHE #
############
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install apache2 libapache2-mod-php5 php5-mysql php5-gd php-pear php-apc php5-curl curl lynx-cur

# Enable apache mods.
RUN a2enmod php5
RUN a2enmod rewrite
RUN a2enmod cgi

# Update the PHP.ini file, enable <? ?> tags and quieten logging.
RUN sed -i "s/short_open_tag = Off/short_open_tag = On/" /etc/php5/apache2/php.ini
RUN sed -i "s/error_reporting = .*$/error_reporting = E_ERROR | E_WARNING | E_PARSE/" /etc/php5/apache2/php.ini

# Manually set up the apache environment variables
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid

EXPOSE 80

# Update the default apache site with the config we created.
ADD apache-config.conf /etc/apache2/sites-enabled/000-default.conf

###########
# PYTHON #
###########
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install python2.7 python-setuptools python-pip

###########
# GIT #
###########
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install git

###############
# ACI Toolkit #
###############
WORKDIR /opt
RUN git clone https://github.com/datacenter/acitoolkit.git
WORKDIR /opt/acitoolkit
RUN python setup.py install

#########
# Install Tige's Stuff!  Web2ACI
#########
RUN mv /var/www/html/index.html /var/www
RUN mkdir /var/www/cgi-bin
ADD cgi-bin /var/www/cgi-bin
ADD www /var/www
ADD credentials.py /usr/lib/python2.7/dist-packages/

# By default when this container runs, simply start apache.
CMD /usr/sbin/apache2ctl -D FOREGROUND
