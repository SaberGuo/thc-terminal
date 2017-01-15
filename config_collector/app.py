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
from commons.commons import upload_count,tcpc_dst_url,tcpc_dst_port,self_ip,self_mask,self_gateway,check_json_format
import threading
import wiznet_wrapper.wiznet as wiz
from wiznet_wrapper import WIZNET_GOT_DATA,WIZNET_READY
from commons.gpio_ctrl import *
import socket
import json
import time
import sys
import os

def init_tcpc():
    wiz.init_hardware()
    wiz.init_conf(self_ip, self_mask, self_gateway)

crontab_dict = {'img_capture_invl': 'python app.py #img_capture_invl',
                'img_upload_invl':'python app.py #img_upload_invl',
                'data_capture_invl':'python app.py #data_capture_invl',
                'data_upload_invl':'python app.py #data_upload_invl'}
def deal_single_crontab(key, value):
    if config._is_debug:
        print "deal single crontab:{0},{1},{2}".format(key, value, crontab_dict[key])
    else:
        os.system('./change_single_crontab.sh "{0}" "{1} {2}"'.key, value, crontab_dict[key])

def deal_crontab(new_control, old_control):
    for key,value in new_control.items():
        if value !=old_control[key]:
            deal_single_crontab(key,value)

def deal_config(new_config):
    config.get_instance().update_config(new_config)

def test_proc():
    print "start test_proc"
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((config._debug_ip, config._debug_port))
    try:
        server_socket.listen(1)
    except socket.error, e:
        print "test_proc: fail to listen on port %s"%e
        sys.exit(1)
    while True:
        print "test_proc: waiting for connection..."
        client, addr = server_socket.accept()
        data = client.recv(1024)
        print "test_proc: recieve data:" + data
        print "test_proc: send data back"
        cf = open("./config.json","r")
        data = json.load(cf)
        client.sendall(json.dumps(data))
        client.close()

def recv_proc(event, ready_event, test_suit):
    p =socket.gethostbyname(tcpc_dst_url)
    cf = config.get_instance()
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
        if res is not None and check_json_format(res):
            jres = json.loads(res)
            print "recv_proc:receive data:",jres
            if jres.has_key("device_id") \
                and jres.has_key("device_config_id") \
                and jres.has_key("method") and jres['method'] == 'push_param'\
                and jres.has_key("config")\
                and jres.has_key("control"):
                deal_config(jres)
                deal_crontab(jres['control'], cf.ctrl_config)
                event.set()

def main_proc(event,ready_event, test_suit):
    cf = config.get_instance()
    up_dict = {'device_id': cf.get_device_id(),
               'method':'pull_param'}
    jup_dict = json.dumps(up_dict)
    if config._is_debug:
        test_suit.send(jup_dict)
    else:
        ready_event.wait(5)
        if ready_event.is_set():
            wiz.send(jup_dict, len(jup_dict))
    event.wait(5)

if __name__ == "__main__":
    power_ctrl_init()
    net_power_ctrl()
    timer_proc(200)
    et = threading.Event()
    rt = threading.Event()
    init_tcpc()
    #test setting
    test_suit = None
    if config._is_debug:
        test_suit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    rt = threading.Thread(target=recv_proc, args=(et, rt, test_suit))
    mt = threading.Thread(target=main_proc, args=(et, rt, test_suit))
    rt.setDaemon(True)
    rt.start()
    mt.start()
    mt.join()
