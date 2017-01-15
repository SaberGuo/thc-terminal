#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/10
"""
import json


class config(object):
    conf_file_path = "../data/config.json"
    instance = None
    min_s = 4000.0
    max_s = 65535.0
    _is_debug = True
    _debug_ip = "127.0.0.1"
    _debug_port = 6000

    def __init__(self):
        self.cf = file(self.conf_file_path)
        self.cf_dict = json.load(self.cf)
        self.device_id = self.cf_dict['device_id']
        self.device_config_id = self.cf_dict['device_config_id']
        self.data_config = self.cf_dict['config']
        self.ctrl_config = self.cf_dict['control']


    def __str__(self):
        return json.dumps(self.cf_dict)
    @staticmethod
    def get_instance():
        if config.instance == None:
            config.instance = config()
        return config.instance

    def parse_numeric_data(self, value, port):
        for data_key, data_item in self.data_config.items():
            if data_item['port'] == port:
                max_v = data_item['max_v']
                min_v = data_item['min_v']
                res = (value-self.min_s)/(self.max_s-self.min_s)*(max_v-min_v)+min_v
                return (data_key, res)
        return (None,None)

    def get_ctrl_val(self, key):
        if key in self.ctrl_config.keys():
            return self.ctrl_config[key]
        return None

    def get_device_id(self):
        return self.device_id
    def get_device_config_id(self):
        return self.device_config_id
    def get_img_capture_invl(self):
        return self.get_ctrl_val('img_capture_invl')

    def get_img_upload_invl(self):
        return self.get_ctrl_val('img_upload_invl')

    def get_data_capture_invl(self):
        return self.get_ctrl_val('data_capture_invl')

    def get_data_upload_invl(self):
        return self.get_ctrl_val('data_upload_invl')


