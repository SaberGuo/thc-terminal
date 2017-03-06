#! /bin/bash

base_root='/home/pi/thc-terminal/'
data_uploader_name='data_uploader/'
img_collector_name='img_collector/'
config_collector_name='config_collector/'
command='start.sh'


cd ${base_root}${img_collector_name}
flock -e -w100 /tmp/wiznet.lock -c "echo 'img collector!'; sudo python app.py"
