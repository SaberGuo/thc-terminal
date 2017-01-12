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
from wiznet_wrapper import WIZNET_GOT_DATA
from commons.gpio_ctrl import *
import socket
import json

global is_uploaded
def init_tcpc():
    wiz.init_hardware()
    wiz.init_conf(self_ip, self_mask, self_gateway)

def recv_proc(event):
    p =socket.gethostbyname(tcpc_dst_url)
    cf = config.get_instance()
    while True:
        ret = wiz.loopback_tcpc(0,str(p),tcpc_dst_port)
        if ret == WIZNET_GOT_DATA:
            res = wiz.tcpc_recv(1024)
            if res is not None and check_json_format(res):
                jres = json.loads(res)
                if jres.has_key("device_id") \
                    and jres.has_key("device_config_id") \
                    and jres.has_key("method") and jres['method'] == 'push_param'\
                    and jres.has_key("config")\
                    and jres.has_key("control"):
                        pass
                event.set()

def main_proc(event):
    global is_uploaded
    is_uploaded = False
    cf = config.get_instance()
    up_dict = {'device_id': cf.get_device_id(),
               'method':'pull_param'}
    jup_dict = json.dumps(up_dict)
    wiz.send(jup_dict, len(jup_dict))
    event.wait(5)

if __name__ == "__main__":
    power_ctrl_init()
    net_power_ctrl()
    timer_proc(200)

    init_tcpc()
    et = threading.Event()
    #start socket
    rt = threading.Thread(target=recv_proc, args=(et))
    mt = threading.Thread(target=main_proc, args=(et))
    rt.setDaemon(True)
    rt.start()
    mt.start()
    mt.join()
