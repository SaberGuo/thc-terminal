#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/10
"""
from commons import timer_proc
import RPi.GPIO as gpio

DSP_POWER_CTRL_GPIO = 13
AD_POWER_CTRL_GPIO = 17
TIME_FOR_RELAYER = 210

def power_ctrl_init():
    gpio.setmode(gpio.BCM)
    gpio.setup(DSP_POWER_CTRL_GPIO, gpio.OUTPUT)
    gpio.setup(AD_POWER_CTRL_GPIO, gpio.OUTPUT)
    gpio.output(DSP_POWER_CTRL_GPIO, gpio.LOW)
    gpio.output(AD_POWER_CTRL_GPIO, gpio.LOW)

def power_ctrl(pin):
    gpio.output(pin, gpio.LOW)
    timer_proc(TIME_FOR_RELAYER)
    gpio.output(pin, gpio.HIGH)
    timer_proc(TIME_FOR_RELAYER)
    gpio.output(pin, gpio.LOW)


def dsp_power_ctrl():
    power_ctrl(DSP_POWER_CTRL_GPIO)

def ad_power_ctrl():
    power_ctrl(AD_POWER_CTRL_GPIO)