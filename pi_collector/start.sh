#! /bin/bash

base_root='/home/pi/thc-terminal/'
data_uploader_name='data_uploader/'
img_collector_name='img_collector/'
config_collector_name='config_collector/'
pi_collector_name='pi_collector/'
command='start.sh'


cd ${base_root}${pi_collector_name}
python app.py

