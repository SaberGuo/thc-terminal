#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/10
"""
import RPi.GPIO as gpio

from commons.commons import timer_proc

DSP_POWER_CTRL_GPIO = 13
AD_POWER_CTRL_GPIO = 17
NET_POWER_CTRL_GPIO = 20
CAMDERA_POWER_CTRL_GPIO = 23

ALARM_CTRL_GPIO = 21

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

def net_power_ctrl():
    power_ctrl(NET_POWER_CTRL_GPIO)

def camera_power_ctrl():
    power_ctrl(CAMDERA_POWER_CTRL_GPIO)


def alarm_on():
    gpio.output(ALARM_CTRL_GPIO, gpio.HIGH)

def alarm_off():
    gpio.output(ALARM_CTRL_GPIO, gpio.LOW)