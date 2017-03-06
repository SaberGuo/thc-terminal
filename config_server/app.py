#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/2/10
"""
import conclude
from commons.data_pool import data_pool
from commons.conf import config
from commons.gpio_ctrl import *
import json
from commons.commons import max_count,tcp_server_port,self_ip,self_mask,self_gateway,get_file_size,tcp_server_sn, timer_proc
from commons.commons import check_json_format
from wiznet_wrapper import *
import wiznet_wrapper.wiznet as wiz
import os
def update_config(content):
    config.get_instance().update_config(content)

def reboot_dev(content):
    os.system("sudo reboot")

def deal_method(post):
    methods = {'update_config': update_config,
               'reboot': reboot_dev}
    methods[post['methods']](post['content'])

def main_proc():
    count = 0
    is_connected = False
    while count <max_count or is_connected:
        count+=1
        ret = wiz.loopback_tcps(tcp_server_sn, tcp_server_port)
        if ret == 2:
            res = wiz.tcps_recv(1024)
            if res is not None and len(res)>0:
                is_connected = True
                if check_json_format(res):
                    jres = json.loads(res)
                    if jres.has_key('method') and jres.has_key('content'):
                        deal_method(jres)



if __name__ == "__main__":
    power_ctrl_init()
    setup_driver()
    net_power_ctrl("on")
    out_power_ctrl("off")
    timer_proc(200)
    init_tcpc(self_ip, self_mask, self_gateway)

    main_proc()

    net_power_ctrl("off")
    #setdown_driver()
