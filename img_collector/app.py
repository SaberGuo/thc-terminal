#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/2/9
"""
import conclude
from commons.gpio_ctrl import *
from commons.commons import upload_count,tcpc_dst_url,tcpc_dst_port,self_ip,self_mask,self_gateway,get_file_size,img_up_sn, timer_proc,dns_sn,once_send_size
from wiznet_wrapper import *
from wiznet_wrapper import wiznet as wiz 
from commons.data_pool import data_pool
from commons.conf import config
import json
import os


def main_proc():
    print "start img upload"
    print dns_sn, tcpc_dst_url
    p =gethostname(dns_sn, tcpc_dst_url)
    print dns_sn, tcpc_dst_url
    if len(p)==0:
        print "exit for main proc"
        return
    #p = tcpc_dst_url
    if establish_connect(img_up_sn, p, tcpc_dst_port) == 0:
        print "establish error, 26"
        return
    cf = config.get_instance()
    up_dict = {'device_id':cf.get_device_id(),
               'device_config_id':cf.get_device_config_id(),
               'method':'push_image'}
    dp = data_pool.get_instance()
    imgs = dp.get_imgs(upload_count)
    for img in imgs:
        up_dict['key'] = img[1]
        up_dict['size'] = get_file_size(img[2])
        up_dict['acquisition_time'] = img[0]
        jup_dict = json.dumps(up_dict)
        print jup_dict
        if 0 == send_data(img_up_sn, p, tcpc_dst_port, jup_dict, len(jup_dict)):
            print "error for send data, 39"
            return
        res = recv_data(img_up_sn, p, tcpc_dst_port)
        if res == None:
            print "recv error, 44"
            return
        jres = json.loads(res)
        print jres
        if not jres.has_key('method') or jres['method'] != "push_image_ready":
            print "error for recv data, 46"
            return
        f = open(img[2],'rb')
        jres = None
        chunk_size = get_file_size(img[2])
        tmp_size = 0
        for i in range(chunk_size/once_send_size):
            chunk = f.read(once_send_size)
            last_len = send_data(img_up_sn, p, tcpc_dst_port, chunk, len(chunk))
            if last_len == 0:
                print "error for send data, 55"
                return
            tmp_size = tmp_size+len(chunk)

        chunk = f.read(once_send_size)
        if len(chunk)>0:
            last_len = send_data(img_up_sn, p, tcpc_dst_port, chunk, len(chunk))
            if last_len == 0:
                print "error for send data, 61"
                return
        tmp_size = tmp_size+len(chunk)
        print "send data size:",tmp_size

        res = recv_data(img_up_sn,p, tcpc_dst_port)
        if res == None:
            print "recv error, 70"
            return
        jres = json.loads(res)
        if jres.has_key('method') and jres['method'] == 'image_uploaded':
            print "main_proc:image uploaded"
            dp.del_img([img])
            os.remove(img[2])

    up_dict = {'device_id': cf.get_device_id(),
                'method': 'close_connection'}
    print up_dict
    if 0 == send_data(img_up_sn, p, tcpc_dst_port, json.dumps(up_dict),len(json.dumps(up_dict))):
        print "send error, 79"
        return

if __name__ == "__main__":
    power_ctrl_init()
    setup_driver()
    out_power_ctrl("on")
    timer_proc(100000)
    net_power_ctrl("on")
    timer_proc(200)
    net_reset()
    timer_proc(1000)
    alarm_on()
    os.system("./img_col.sh") #save img
    #print "img collected\n\n\n"
    alarm_off()
    timer_proc(1000)
    net_reset()
    timer_proc(2000)
    init_tcpc(self_ip, self_mask, self_gateway)
    timer_proc(2000)
    main_proc() #upload img
    timer_proc(2000)
    net_power_ctrl("off")
    out_power_ctrl("off")
    setdown_driver()

