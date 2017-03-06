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
import json
from commons.commons import upload_count,tcpc_dst_url,tcpc_dst_port,self_ip,self_mask,self_gateway,get_file_size,data_up_sn,dns_sn,timer_proc
from wiznet_wrapper import *
import wiznet_wrapper.wiznet as wiz
import time



def main_proc():
    dp = data_pool.get_instance()
    upload_values = dp.get_data(upload_count)
    if len(upload_values) == 0:
        return
    #p =gethostname(dns_sn, tcpc_dst_url)
    #if len(p)==0:
    #    return
    p = tcpc_dst_url    
    print tcpc_dst_url    
    if establish_connect(data_up_sn, p, tcpc_dst_port) == 0:
        print "not established"
        return
    cf = config.get_instance()
    up_dict = {'device_id': cf.get_device_id(),
               'device_config_id':cf.get_device_config_id(),
               'method':'push_data',
               'package':{}}
    upload_values = dp.get_data(upload_count)
    for uv in upload_values:
        up_dict['package'][uv[0]] = json.loads(uv[1])
    jup_dict = json.dumps(up_dict)
    print "main proc up dict:",len(jup_dict)
    if 0 == send_data(data_up_sn, p, tcpc_dst_port, jup_dict, len(jup_dict)):
        print "send data error"
        return
    res = recv_data(data_up_sn,p, tcpc_dst_port)
    if res == None:
        print "replay is none"
        return
    try:
        jres = json.loads(res)
        print "server replay:",jres
        res = None
        if jres.has_key('method') and jres['method'] == 'data_uploaded':
            dp.del_data(upload_values)
            return
    except Exception as e:
        print e
    wiz.socket_disconnect(data_up_sn)
    wiz.socket_close(data_up_sn)

     

if __name__ == "__main__":
    power_ctrl_init()
    setup_driver()
    out_power_ctrl("on")
    #timer_proc(70000)
    timer_proc(700)
    net_power_ctrl("on")
    timer_proc(2000)
    net_reset()
    timer_proc(2000)
    init_tcpc(self_ip, self_mask, self_gateway)
    timer_proc(200)
    main_proc()
    net_power_ctrl("off")
    out_power_ctrl("off")
    #setdown_driver()
