#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/3/8
"""
import conclude
from commons.commons import self_ip, self_mask, self_gateway, timer_proc,dns_sn,tcpc_dst_url
from commons.gpio_ctrl import net_reset,power_ctrl_init,setup_driver,net_power_ctrl,setdown_driver
from wiznet_wrapper import *
if __name__ == "__main__":
    power_ctrl_init()
    setup_driver()
    timer_proc(200)
    net_power_ctrl('on')
    timer_proc(200)
    net_reset()
    timer_proc(200)
    init_tcpc(self_ip, self_mask, self_gateway)
    timer_proc(1000)
    p =gethostname(dns_sn, tcpc_dst_url)
    print p
    net_power_ctrl('off')
    setdown_driver()
