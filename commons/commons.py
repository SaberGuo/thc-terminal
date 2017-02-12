#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/10
"""

import time
import os
import json

upload_count = 10
tcpc_dst_url = "123.57.60.239"
tcpc_dst_port = 7800

data_up_sn = 0
img_up_sn = 1
config_download_sn = 2
dns_sn = 6
tcp_server_sn = 7
tcp_server_port = 8000

self_ip = "192.168.1.119"
self_mask = "255.255.255.0"
self_gateway = "192.168.1.1"


max_count = 50000

def timer_proc(interval_in_millisecond):
    loop_interval = 10      # 定时精度，也是循环间隔时间（毫秒），也是输出信息刷新间隔时间，它不能大于指定的最大延时时间，否则可能导致无任何输出
    t = interval_in_millisecond / loop_interval
    while t >= 0:
        min = (t * loop_interval) / 1000 / 60
        sec = (t * loop_interval) / 1000 % 60
        millisecond = (t * loop_interval) % 1000
        #print('\rThe remaining time:%02d:%02d:%03d...' % ( min, sec, millisecond ), end = '\t\t')
        time.sleep(loop_interval / 1000)
        t -= 1
    if millisecond != 0:
        millisecond = 0
        #print('\rThe remaining time:%02d:%02d:%03d...' % ( min, sec, millisecond ), end = '\t\t')
    #print()

def get_file_size(path):
    try:
        size = os.path.getsize(path)
        return size
    except Exception as err:
        print(err)

def check_json_format(raw_msg):
    """
    用于判断一个字符串是否符合Json格式
    :param self:
    :return:
    """
    if isinstance(raw_msg, str):       # 首先判断变量是否为字符串
        try:
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False
