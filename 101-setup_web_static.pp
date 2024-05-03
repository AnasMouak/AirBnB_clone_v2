# configuring server with Puppet

exec {'install':
  provider => shell,
  command  =>' apt-get -y update ; apt-get -y install nginx ; ufw allow "Nginx HTTP" ; service nginx start ; mkdir -p /data/web_static/releases/test/ ; mkdir -p /data/web_static/shared/ ; echo "Hello!" > /data/web_static/releases/test/index.html ; ln -s /data/web_static/releases/test/ /data/web_static/current ; sudo chown -R ubuntu:ubuntu /data/ ; sed -i "s,server_name _;,server_name _;\n\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}," "/etc/nginx/sites-available/default"; service nginx restart',
}
