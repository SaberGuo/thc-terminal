#!/bin/bash
crontab -l -u pi > ../data/crontab.bak
sed -i '/'${1}'/d' ../data/crontab.bak
echo "${2}" >> ../data/crontab.bak
crontab -u pi ../data/crontab.bak
