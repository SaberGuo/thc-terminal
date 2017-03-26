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
    min_s = 4.0
    max_s = 20.0
    _is_debug = False
    _is_local = False
    _debug_ip = "192.168.1.100"
    _debug_port = 8000

    def __init__(self):
        self.cf = file(self.conf_file_path)
        self.cf_dict = json.load(self.cf)
        self.cf.close()
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
    def update_config(self, jconf):
        self.cf = file(self.conf_file_path,'w')
        str_conf = json.dumps(jconf)
        self.cf.write(str_conf)
        self.cf.flush()
        self.cf.close()
    def get_sensor_data(self, sensor_type, value_i):
        try:
            return getattr(self,sensor_type)(value_i)
        except:
            return 0
    def parse_numeric_data(self, value, port):
        for data_key, data_item in self.data_config.items():
            if data_item['port'] == port:
                device_type = data_item['sensor_type']
                res = self.get_sensor_data(device_type, value)

                max_v = data_item['max_v']
                min_v = data_item['min_v']
                if res >max_v:
                    res = max_v
                if res <min_v:
                    res = min_v
                #res = (value-self.min_s)/(self.max_s-self.min_s)*(max_v-min_v)+min_v
                return (data_key, res)
        return (None,None)

    def get_port_key(self, port):
        for data_key, data_item in self.data_config.items():
            if data_item['port'] == port:
                return data_key
        return None

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

    #for device_type methods
    def SOILMTYXR1_H(self, value):
        return 6.25*value-25
    def SOILMTYXR1_T(self, value):
        return 6.25*value-55
    def CWS1806A1AG_H(self, value):
        return (value-4)/16*(100)-0
    def CWS1806A1AG_T(self, value):
        return (value-4)/16*(60+20)-20
    def NHZD1CI_S(self, value):
        return (value-4)/16*200000-0
    def NHFS45B1_WS(self, value):
        return (value-4)/16*(60-0)-0
    def NHFX46A1_WD(self, value):
        return (value-4)/16*(360-0)-0
    def KAVT2_V(self, value):
        return (value-4)/16*(25-0)-0

if __name__ == "__main__":
    cf = config.get_instance().get_port_key("Img1")
    print cf
