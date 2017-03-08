#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/3/8
"""
import conclude
from data_collector.uart import uart_controller
from commons.commons import timer_proc
from commons.gpio_ctrl import power_ctrl_init,setup_driver,ad_power_ctrl,setdown_driver
if __name__ == "__main__":
    power_ctrl_init()
    setup_driver()
    timer_proc(200)
    ad_power_ctrl('on')
    timer_proc(2000)
    ut = uart_controller.get_instance()
    ut.uart_open()
    rtt = ut.read_ad_values()
    print "read res:", rtt
    ad_power_ctrl('off')
    setdown_driver()