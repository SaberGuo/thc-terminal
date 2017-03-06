#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/10
"""
import conclude
from build_msg import *
from commons.commons import timer_proc
from commons.data_pool import data_pool
from commons.gpio_ctrl import power_ctrl_init, dsp_power_ctrl,ad_power_ctrl,setup_driver, setdown_driver
from uart import uart_controller


def main():
    #power on for dsp and ad
    #construct the database item
    uc = uart_controller.get_instance()
    uc.uart_open()
    ads_v = uc.read_ad_values()
    print ads_v
    data_str = build_msg(ads_v)
    print data_str
    dp = data_pool.get_instance()
    dp.save_data(int(time.time()),data_str)




if __name__ == "__main__":
    power_ctrl_init()
    setup_driver()
    dsp_power_ctrl("on")
    timer_proc(20000)
    main()
    timer_proc(200)
    dsp_power_ctrl("off")
    setdown_driver()

