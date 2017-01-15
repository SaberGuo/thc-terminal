#!/bin/bash

crontab -l > /tmp/crontab.bak
sed -i '/'"$1"'/d' /tmp/crontab.bak
echo '"$2"' >> /tmp/crontab.bak
crontab /tmp/crontab.bak