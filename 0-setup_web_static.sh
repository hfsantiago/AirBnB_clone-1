#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static

# Instaling nginx
apt upgrade -y
apt install nginx -y

# Creating directories
mkdir -p /data/web_static/{releases/test,shared}

# Fake html
echo "\
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# Symbolic link 
ln -sfn /data/web_static/releases/test/ /data/web_static/current

# Changing user ang group
chown -R ubuntu:ubuntu /data 

# Setting /hbnb_static for serve static
CONTENT="\\\tlocation /hbnb_static {\n\
	\talias /data/web_static/current/;\n\
	\tautoindex off;\n\
	}"

sed -i "31i $CONTENT" /etc/nginx/sites-available/default

service nginx restart
