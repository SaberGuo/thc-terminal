#! /bin/bash

cd /home/pi/thc-terminal/data_collector
flock -e -w160 /tmp/wiznet.lock -c "sudo python app.py"
