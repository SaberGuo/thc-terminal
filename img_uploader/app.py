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

import json
import socket
from commons.commons import upload_count,tcpc_dst_url,tcpc_dst_port,self_ip,self_mask,self_gateway,get_file_Size
import threading
import wiznet_wrapper.wiznet as wiz
from wiznet_wrapper import WIZNET_GOT_DATA

jres = None

def init_tcpc():
    wiz.init_hardware()
    wiz.init_conf(self_ip, self_mask, self_gateway)

def recv_proc(event):
    global jres
    p =socket.gethostbyname(tcpc_dst_url)
    while True:
        ret = wiz.loopback_tcpc(0,str(p),tcpc_dst_port)
        if ret == WIZNET_GOT_DATA:
            res = wiz.tcpc_recv(1024)
            if res is not None:
                jres = json.loads(res)
                event.set()


def main_proc(event):
    global jres
    cf = config.get_instance()
    up_dict = {'device_id':cf.get_device_id(),
               'device_config_id':cf.get_device_config_id(),
               'method':'push_image'}
    dp = data_pool.get_instance()
    imgs = dp.get_imgs(10)
    for img in imgs:
        up_dict['key'] = img[1]
        up_dict['size'] = get_file_Size(img[2])
        up_dict['acquisition_time'] = img[0]
        wiz.socket_send(json.dumps(up_dict))
        event.wait(3)
        if event.is_set() and jres is not None and  jres.has_key('method') and jres['method'] == 'push_image_ready':
            f = open(img[2],'rb')
            jres = None
            chunk = f.read()
            wiz.socket_send(0, chunk, len(chunk))
            event.wait(3)
            if event.is_set() and jres is not None and jres.has_key('method') and jres['method'] == 'image_uploaded':
                dp.del_img(img)

if __name__ == "__main__":
    et = threading.Event()
    mp = threading.Thread(target=main_proc, args=(et))
    rp = threading.Thread(target=recv_proc, args=(et))
    rp.start()
    mp.start()
    mp.join()