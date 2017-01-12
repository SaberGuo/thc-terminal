#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/11
"""

import conclude
from commons.gpio_ctrl import power_ctrl_init,camera_power_ctrl,alarm_on,alarm_off
from commons.commons import timer_proc


if __name__ == "__main__":
    #camera power on and wait for the while
    power_ctrl_init()
    camera_power_ctrl()
    timer_proc(40000)
    #alarm set
    alarm_on()
    timer_proc(1000)
    alarm_off()
    #wait for while
    timer_proc(10000)
    #camera power off
    camera_power_ctrl()