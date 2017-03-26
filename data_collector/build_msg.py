#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/11
"""
import json
import time

from commons.data_pool import data_pool
from commons.conf import config
from commons.commons import every_tip_parts
import re


def build_msg(ads_v):
    data = build_ads(ads_v)

    pi_key, pi_content = build_PI()
    if pi_key is not None and pi_content is not None:
        data[pi_key] = pi_content
    print "res for data:", data
    return json.dumps(data)

def build_ads(ads_v):
    cf = config.get_instance()
    res = {}
    for i in range(len(ads_v)):
        ad_port = "AD{0}".format(i+1)
        ad_key, ad_rv = cf.parse_numeric_data(ads_v[i],ad_port)
        if ad_key is not None and ad_rv is not None:
            res[ad_key] = {'value': round(ad_rv,2)}
    return res


def build_PI():
    dp = data_pool.get_instance()
    pi_v = dp.get_pi_value()
    pi_port_re = re.compile('^PI\d+')
    cf = config.get_instance()
    for key, content in cf.data_config.items():
        if pi_port_re.match(content['port']) is not None:
            return (key, {'value':pi_v*every_tip_parts})
    return (None,None)
