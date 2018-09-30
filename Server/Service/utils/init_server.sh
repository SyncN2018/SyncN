if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

projectname=syncn

# install erlang for rabbitmq
wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb $ sudo dpkg -i erlang-solutions_1.0_all.deb
apt-get update
apt-get install -y erlang

# install rabbitmq
apt-get install -y rabbitmq-server
rabbitmq-plugins enable rabbitmq_management
service rabbitmq-server restart

# add user & remove default user
rabbitmqctl delete_user guest
rabbitmqctl add_user $projectname $projectname
rabbitmqctl add_vhost $projectname
rabbitmqctl set_user_tags $projectname administrator
rabbitmqctl set_permissions -p / $projectname ".*" ".*" ".*"

wget https://raw.githubusercontent.com/rabbitmq/rabbitmq-management/master/bin/rabbitmqadmin
chmod 755 rabbitmqadmin
cp rabbitmqadmin /usr/bin/
rm ./rabbitmqadmin

rabbitmqadmin -u {$projectname} -p {$projectname} -V {$projectname} declare exchange name='cmd' type='topic'
rabbitmqadmin -u {$projectname} -p {$projectname} -V {$projectname} declare exchange name='msg' type='topic'

# install pm2 for nodejs
pm2 install pm2-logrotate
pm2 install pm2 -g

# setting pm2
pm2 set pm2-logrotate:max_size 1M
pm2 set pm2-logrotate:interval_unit DD
pm2 set pm2-logrotate:reatain 10

# install nodejs10.x
apt-get install -y nodejs


curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add - 
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list 
apt-get update 
apt-get install -y yarn
apt autoremove

