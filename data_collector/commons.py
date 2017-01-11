#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/10
"""

import time

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