#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/3/8
"""

import conclude
import sys
from commons.gpio_ctrl import *

sign_names = ['net', 'ad', 'out']
sign_actions = ['on', 'off']

def print_usage():
    print "usage: python power_test.py [name] [action]"
    print "[name] includes: net, ad, out"
    print "[action] on-means power on; off-means power off"
    print "eg. python power_test.py net on--means make the net power on"
if __name__ == "__main__":
    if len(sys.argv)!=3:
        print_usage()

    name = sys.argv[1]
    action = sys.argv[2]

    if name not in sign_names or action not in sign_actions:
        print_usage()

    power_ctrl_init()
    setup_driver()
    eval(name+'_power_ctrl')(action)
