#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/10
"""
from power_ctrl import power_ctrl_init, dsp_power_ctrl,ad_power_ctrl
from data_pool import data_pool
from commons import timer_proc
from uart import uart_controller
from build_msg import *

def main():
    #power on for dsp and ad
    power_ctrl_init()
    dsp_power_ctrl()
    ad_power_ctrl()
    timer_proc(200)
    #construct the database item
    uc = uart_controller.get_instance()
    uc.uart_open()
    ads_v = uc.read_ad_values()
    data_str = build_msg(ads_v)
    dp = data_pool.get_instance()
    dp.save_data(time.time(),data_str)
    #off the power
    dsp_power_ctrl()
    ad_power_ctrl()




if __name__ == "__main__":
    main()