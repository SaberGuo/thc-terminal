#! /bin/bash

base_root='/home/pi/thc-terminal/'
data_uploader_name='data_uploader/'
img_uploader_name='img_uploader/'
config_collector_name='config_collector/'
ftp_server_name = 'ftp_server/'
command='start.sh'


cd ${base_root}${ftp_server_name}
sudo python app.py