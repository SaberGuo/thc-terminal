#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/2/10
"""

import socket
import commons.commons.tcp_server_port as server_port
import commons.commons.self_ip as server_ip
import sys, os
import json

BUFFER_SIZE = 1024

if __name__ == "__main__":
    if len(sys.argv)!=2 and len(sys.argv)!=3:
        print "usage: python app_client.py 'reboot'"
        print "usage: python app_client.py 'update_config' '<path/config.conf>'"
        sys.exit(0)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_port, server_ip))
    s.send('start')
    data = s.recv(BUFFER_SIZE)
    print "server connected and msg is:",data
    if len(sys.argv) == 2 and sys.argv[1] == 'reboot':
        jres = {'method':'reboot','content':''}
        s.send(json.dumps(jres))
        data = s.recv(BUFFER_SIZE)
        print "server connected and msg is:",data

    if len(sys.argv) == 3 and sys.argv[1] == 'update_config' and os.path.exists(sys.argv[2]):
        jres = {'method':'update_config','content':''}
        f = open(sys.argv[2],'r')
        ct = f.readall()
        try:
            jct = json.loads(ct)
            print "config content is"
            print ct
            while True:
                res = raw_input("confirm or cancel the update(y/n):")
                if res.strip() == 'y':
                    jres['content'] = ct
                    s.send(json.dumps(jres))
                    data = s.recv(BUFFER_SIZE)
                    print "server connected and msg is:",data
                    print "config updated"
                    break

                if res.strip() == 'n':
                    print "cancel the updating"
                    break
                print "input wrong"

        except:
            print "conf structure error!"





