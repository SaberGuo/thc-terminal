#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/11
"""

import RPi.GPIO as gpio
import threading
from commons.data_pool import data_pool
from commons.commons import timer_proc
import time

PI_IN_GPIO = 20
PI_counts = 0

def interrupt_proc(locker):
    global PI_counts
    gpio.setmode(gpio.BCM)
    gpio.setup(PI_IN_GPIO, gpio.IN, pull_up_down=gpio.PUD_UP)
    while True:
        gpio.wait_for_edge(25, gpio.FALLING)
        locker.acquire()
        PI_counts = PI_counts+1
        locker.release()


def main_proc(locker):
    global PI_counts
    dp = data_pool.get_instance()
    while True:
        locker.acquire()
        if PI_counts>0:
            dp.save_pi(time.time(), PI_counts)
            PI_counts = 0
        locker.release()
        timer_proc(10000)

if __name__ == "__main__":
    lk = threading.Lock()
    mp = threading.Thread(target=main_proc, args=(lk))
    ip = threading.Thread(target=interrupt_proc, args=(lk))
    mp.start()
    ip.start()
    mp.join()
    ip.join()