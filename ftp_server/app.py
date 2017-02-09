#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/2/9
"""

from commons.gpio_ctrl import *
import os

if __name__ == "__main__":
    power_ctrl_init()
    setup_driver()
    net_power_ctrl("on")
    timer_proc(200)
    net_reset()
    camera_power_ctrl("on")
    timer_proc(40000)
    alarm_on()
    os.system("sudo ./build/ftp_server")
    alarm_off()
    camera_power_ctrl("off")
    net_power_ctrl("off")
    setdown_driver()

