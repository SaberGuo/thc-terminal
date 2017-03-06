#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/11
"""
import wiznet as wiz

WIZNET_GOT_DATA = 2
WIZNET_READY = 3
WIZNET_TIMEOUT = -13
def init_tcpc(self_ip,self_mask,self_gateway):
    wiz.init_hardware()
    wiz.init_conf(self_ip, self_mask, self_gateway)

def gethostname(sn, host):
    ret = wiz.dns_host_to_ip(sn, host)
    if ret>0:
        return wiz.dns_get_ip(1024)
    else:
        print "dns parse failed!"
        return ""
def establish_connect(sn, ip, port):
    count = 0
    while True:
        ret = wiz.loopback_tcpc(sn,ip,port)
        if ret == WIZNET_READY:
            return 1
        else:
            count = count+1
            if count>20:
                return 0

def recv_data(sn,ip, port):
    res = None
    while True:
        ret = wiz.loopback_tcpc(sn,ip,port)
        if ret == WIZNET_TIMEOUT:
            return res
        if ret == WIZNET_GOT_DATA:
            res = wiz.tcpc_recv(1024)
            if res is not None and len(res)>0:
                return res
def send_data(sn,ip, port, chunk, length_chunk):
    count = 0
    while True:
        ret = wiz.socket_send(sn, ip, port, chunk, length_chunk)
        if ret == length_chunk:
            return 1
        count = count+1
        if count>5:
            return 0
