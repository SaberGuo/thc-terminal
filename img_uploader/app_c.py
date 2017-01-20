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
import time
import json
import socket
from commons.commons import upload_count,tcpc_dst_url,tcpc_dst_port,self_ip,self_mask,self_gateway,get_file_size,img_up_sn
import threading
from wiznet_wrapper import *
import sys

jres = None


def main_proc():
    p =socket.gethostbyname(tcpc_dst_url)
    if establish_connect(img_up_sn, p, tcpc_dst_port) == 0:
        return
    cf = config.get_instance()
    up_dict = {'device_id':cf.get_device_id(),
               'device_config_id':cf.get_device_config_id(),
               'method':'push_image'}
    dp = data_pool.get_instance()
    imgs = dp.get_imgs(1)
    for img in imgs:
        up_dict['key'] = img[1]
        up_dict['size'] = get_file_size(img[2])
        up_dict['acquisition_time'] = img[0]
        jup_dict = json.dumps(up_dict)
        if 0 == send_data(img_up_sn, p, tcpc_dst_port, jup_dict, len(jup_dict)):
            return
        f = open(img[2],'rb')
        jres = None
        chunk_size = get_file_size(img[2])
        tmp_size = 0
        for i in range(chunk_size/1024):
            chunk = f.read(1024)
            if 0 == send_data(img_up_sn, p, tcpc_dst_port, chunk, len(chunk)):
                return
            tmp_size = tmp_size+len(chunk)

        chunk = f.read(1024)
        if 0 == send_data(img_up_sn, p, tcpc_dst_port, chunk, len(chunk)):
            return
        tmp_size = tmp_size+len(chunk)
        print "send data size:",tmp_size

        res = recv_data(img_up_sn,p, tcpc_dst_port)
        if res == None:
            return
        jres = json.loads(res)
        if jres.has_key('method') and jres['method'] == 'image_uploaded':
            print "main_proc:image uploaded"
            #dp.del_img(img)
    up_dict = {'device_id': cf.get_device_id(),
                'method': 'close_connection'}
    if 0 == send_data(img_up_sn, p, tcpc_dst_port, json.dumps(up_dict),len(json.dumps(up_dict))):
        return
     

if __name__ == "__main__":
    init_tcpc(self_ip, self_mask, self_gateway)
    main_proc()
