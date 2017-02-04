#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/10
"""
import RPi.GPIO as gpio

from commons import timer_proc

DSP_POWER_CTRL_GPIO = 13
AD_POWER_CTRL_GPIO = 17
NET_POWER_CTRL_GPIO = 6
CAMERA_POWER_CTRL_GPIO = 23

POWER_DRIVER_CTRL_GPIO_1 = 17
POWER_DRIVER_CTRL_GPIO_2 = 27

NET_RESET_CTRL_GPIO = 24

ALARM_CTRL_GPIO = 21

TIME_FOR_RELAYER = 210

def power_ctrl_init():
    gpio.setmode(gpio.BCM)
    gpio.setup(POWER_DRIVER_CTRL_GPIO_2, gpio.OUT)
    gpio.setup(POWER_DRIVER_CTRL_GPIO_1, gpio.OUT)
    gpio.setup(DSP_POWER_CTRL_GPIO, gpio.OUT)
    gpio.setup(AD_POWER_CTRL_GPIO, gpio.OUT)
    gpio.setup(NET_POWER_CTRL_GPIO, gpio.OUT)
    gpio.setup(CAMERA_POWER_CTRL_GPIO, gpio.OUT)
    gpio.setup(ALARM_CTRL_GPIO, gpio.OUT)
    gpio.setup(NET_RESET_CTRL_GPIO, gpio.OUT)
    gpio.output(DSP_POWER_CTRL_GPIO, gpio.LOW)
    gpio.output(AD_POWER_CTRL_GPIO, gpio.LOW)
    gpio.output(NET_POWER_CTRL_GPIO, gpio.LOW)
    gpio.output(CAMERA_POWER_CTRL_GPIO, gpio.LOW)
    gpio.output(ALARM_CTRL_GPIO, gpio.LOW)
    gpio.output(NET_RESET_CTRL_GPIO, gpio.HIGH)

def setup_driver():
    gpio.output(POWER_DRIVER_CTRL_GPIO_1, gpio.LOW)
    gpio.output(POWER_DRIVER_CTRL_GPIO_2, gpio.HIGH)

def setdown_driver():
    gpio.output(POWER_DRIVER_CTRL_GPIO_1, gpio.LOW)
    gpio.output(POWER_DRIVER_CTRL_GPIO_2, gpio.LOW)
def power_ctrl(pin, action):
    if action == "on":
        gpio.output(pin, gpio.HIGH)
    if action == "off":
        gpio.output(pin, gpio.LOW)


def dsp_power_ctrl(action):
    power_ctrl(DSP_POWER_CTRL_GPIO, action)

def ad_power_ctrl(action):
    power_ctrl(AD_POWER_CTRL_GPIO, action)

def net_power_ctrl(action):
    power_ctrl(NET_POWER_CTRL_GPIO, action)

def camera_power_ctrl(action):
    power_ctrl(CAMERA_POWER_CTRL_GPIO, action)

def net_reset():
    power_ctrl(NET_RESET_CTRL_GPIO, "on")
    timer_proc(200)
    power_ctrl(NET_RESET_CTRL_GPIO, "off")
    timer_proc(200)
    power_ctrl(NET_RESET_CTRL_GPIO, "on")
    timer_proc(200)
def alarm_on():
    gpio.output(ALARM_CTRL_GPIO, gpio.HIGH)

def alarm_off():
    gpio.output(ALARM_CTRL_GPIO, gpio.LOW)


