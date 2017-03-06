#! /bin/bash

base_root='/home/pi/thc-terminal/'
config_server_name='config_server'

cd ${base_root}${config_server_name}
sudo python app.py
