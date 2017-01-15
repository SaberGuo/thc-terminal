#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/11
"""

import conclude
from commons.data_pool import data_pool
from commons.conf import config
from commons.commons import timer_proc,upload_count,tcpc_dst_url,tcpc_dst_port,self_ip,self_mask,self_gateway
import threading
import wiznet_wrapper.wiznet as wiz
from wiznet_wrapper import WIZNET_GOT_DATA,WIZNET_READY
from commons.gpio_ctrl import *
import socket
import time
import json
import sys



def init_tcpc():
    wiz.init_hardware()
    wiz.init_conf(self_ip, self_mask, self_gateway)

def test_proc():
    print "start test_proc"
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((config._debug_ip, config._debug_port))
    try:
        server_socket.listen(1)
    except socket.error, e:
        print "fail to listen on port %s"%e
        sys.exit(1)
    while True:
        print "waiting for connection..."
        client, addr = server_socket.accept()
        data = client.recv(1024)
        print "recieve data:" + data
        print "send data back"
        data = json.dumps({'device_id': "123456", 'method':'data_uploaded', 'ts':time.time()})
        client.sendall(data)
        client.close()

def recv_proc(event, ready_event, test_suit):
    print "start recv_proc"
    p =socket.gethostbyname(tcpc_dst_url)
    res = None
    while True:
        if config._is_debug:
            res = test_suit.recv(1024)
        else:
            ret = wiz.loopback_tcpc(0,str(p),tcpc_dst_port)
            if ret == WIZNET_READY:
                ready_event.set()
            if ret == WIZNET_GOT_DATA:
                res = wiz.tcpc_recv(1024)
        if res is not None:
            try:
               jres = json.loads(res)
               print "server replay:",jres
               res = None
               if jres.has_key('method') and jres['method'] == 'data_uploaded':
                  event.set()
            except:
               pass

def main_proc(event, ready_event, test_suit):
    print "start main_proc" 
    cf = config.get_instance()
    up_dict = {'device_id': cf.get_device_id(),
               'device_config_id':cf.get_device_config_id(),
               'method':'push_data',
               'package':{}}
    dp = data_pool.get_instance()
    upload_values = dp.get_data(upload_count)
    for uv in upload_values:
        up_dict['package'][str(uv[0])] = uv[1]
    jup_dict = json.dumps(up_dict)
    if config._is_debug:
        test_suit.send(jup_dict)
    else:
        ready_event.wait(5)
        if ready_event.is_set():
            wiz.send(jup_dict, len(jup_dict))
    event.wait(5)
    if event.is_set():
        dp.del_data(upload_values)

if __name__ == "__main__":
    power_ctrl_init()
    net_power_ctrl()
    timer_proc(200)
    print "power on!"
    init_tcpc()
    et = threading.Event()
    readyt = threading.Event()
    #test setting
    test_suit = None
    if config._is_debug:
        test_suit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if config._is_local:
            tt = threading.Thread(target=test_proc)
            tt.setDaemon(True)
            tt.start()
        try:
            timer_proc(2000)
            test_suit.connect((config._debug_ip, config._debug_port))
        except socket.error:
            print 'fail to setup socket connection'
            exit(1)
  
    #start socket
    rt = threading.Thread(target=recv_proc, args=(et, readyt, test_suit))
    mt = threading.Thread(target=main_proc, args=(et, readyt, test_suit))
    rt.setDaemon(True)
    rt.start()
    mt.start()
    mt.join()
