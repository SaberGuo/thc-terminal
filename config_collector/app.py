#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/11
"""

import conclude
from commons.conf import config
from commons.gpio_ctrl import *
import json
from commons.commons import upload_count,tcpc_dst_url,tcpc_dst_port,self_ip,self_mask,self_gateway,get_file_size,config_download_sn,timer_proc,dns_sn,flock_part
import os
from wiznet_wrapper import *
import wiznet_wrapper.wiznet as wiz

crontab_dict = {'img_capture_invl': flock_part + '\"/home/pi/thc-terminal/ftp_server/start.sh\" #img_capture_invl',
                'img_upload_invl': flock_part + '\"/home/pi/thc-terminal/img_uploader/start.sh\" #img_upload_invl',
                'data_capture_invl':flock_part + '\"/home/pi/thc-terminal/data_collector/start.sh\" #data_capture_invl',
                'data_upload_invl':flock_part + '\"/home/pi/thc-terminal/data_uploader/start.sh\" #data_upload_invl'}
def deal_single_crontab(key, value):
    if config._is_debug:
        print "deal single crontab:{0},{1},{2}".format(key, value, crontab_dict[key])
    else:
        os.system('./change_single_crontab.sh "{0}" "{1} {2}"'.format(key, value, crontab_dict[key]))

def deal_crontab(new_control, old_control):
    try:
        for key,value in new_control.items():
            #if old_control.has_key(key) and value !=old_control[key]:
            if old_control.has_key(key):
                print "key is:",key
                print "value is: ",value
                deal_single_crontab(key,value)
        #os.system("sudo /etc/init.d/cron restart")
    except Exception as e:
        print "error for deal_crontab:",e

def deal_config(new_config):
    config.get_instance().update_config(new_config)


def main_proc():
    p =gethostname(dns_sn, tcpc_dst_url)
    if establish_connect(config_download_sn, p, tcpc_dst_port) == 0:
        return
    print "established!"
    cf = config.get_instance()
    up_dict = {'device_id': cf.get_device_id(),
               'method':'pull_param'}
    jup_dict = json.dumps(up_dict)
    if 0 == send_data(config_download_sn, p, tcpc_dst_port, jup_dict, len(jup_dict)):
        return

    res = recv_data(config_download_sn,p, tcpc_dst_port)
    if res == None:
        return
    try:
        jres = json.loads(res)
        print "server replay:",jres
        res = None
        if jres.has_key("device_id") \
                and jres.has_key("device_config_id") \
                and jres.has_key("method") and jres['method'] == 'push_param'\
                and jres.has_key("config")\
                and jres.has_key("control"):
            deal_config(jres)
            deal_crontab(jres['control'], cf.ctrl_config)
            up_dict = {'device_id': cf.get_device_id(),
               'method':'param_updated'}
            jup_dict = json.dumps(up_dict)
            if 0 == send_data(config_download_sn, p, tcpc_dst_port, jup_dict, len(jup_dict)):
                return
    except:
        pass
    wiz.socket_disconnect(config_download_sn)
    wiz.socket_close(config_download_sn)

if __name__ == "__main__":
    power_ctrl_init()
    setup_driver()
    net_power_ctrl("on")
    timer_proc(200)
    net_reset()
    init_tcpc(self_ip, self_mask, self_gateway)
    main_proc()
    net_power_ctrl("off")
    setdown_driver()
