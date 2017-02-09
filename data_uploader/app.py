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
from commons.gpio_ctrl import *
import time
import json
import socket
from commons.commons import upload_count,tcpc_dst_url,tcpc_dst_port,self_ip,self_mask,self_gateway,get_file_size,data_up_sn,timer_proc
import threading
from wiznet_wrapper import *
import wiznet_wrapper.wiznet as wiz
import sys

jres = None


def main_proc():
    p =socket.gethostbyname(tcpc_dst_url)
    if establish_connect(data_up_sn, p, tcpc_dst_port) == 0:
        return
    cf = config.get_instance()
    up_dict = {'device_id': cf.get_device_id(),
               'device_config_id':cf.get_device_config_id(),
               'method':'push_data',
               'package':{}}
    dp = data_pool.get_instance()
    upload_values = dp.get_data(upload_count)
    for uv in upload_values:
        up_dict['package'][uv[0]] = json.loads(uv[1])
    jup_dict = json.dumps(up_dict)
    print "main proc up dict:",jup_dict
    if 0 == send_data(data_up_sn, p, tcpc_dst_port, jup_dict, len(jup_dict)):
        return
    res = recv_data(data_up_sn,p, tcpc_dst_port)
    if res == None:
        return
    try:
        jres = json.loads(res)
        print "server replay:",jres
        res = None
        if jres.has_key('method') and jres['method'] == 'data_uploaded':
            #dp.del_data(upload_values)
            return
    except:
        pass
    wiz.socket_disconnect(data_up_sn)
    wiz.socket_close(data_up_sn)

     

if __name__ == "__main__":
    power_ctrl_init()
    setup_driver()
    net_power_ctrl("on")
    timer_proc(200)
    net_reset()
    init_tcpc(self_ip, self_mask, self_gateway)
    main_proc()
    net_power_ctrl("off")
    setdown_driver()
