#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/11
"""

import conclude
from commons.data_pool import data_pool
from commons.conf import config
import time
import json
import socket
from commons.commons import upload_count,tcpc_dst_url,tcpc_dst_port,self_ip,self_mask,self_gateway,get_file_size
import threading
import wiznet_wrapper.wiznet as wiz
from wiznet_wrapper import WIZNET_GOT_DATA, WIZNET_READY
import sys

jres = None

def init_tcpc():
    wiz.init_hardware()
    wiz.init_conf(self_ip, self_mask, self_gateway)

def test_proc():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((config._debug_ip, config._debug_port))
    try:
        server_socket.listen(1)
    except socket.error, e:
        print "fail to listen on port %s"%e
        sys.exit(1)
    recv_size = 0
    is_start_recv_img = False
    print "test_proc: waiting for connection..."
    client, addr = server_socket.accept()
    print "test_proc: connected"
    while True:
        data = client.recv(1024)
        print "test_proc: recieve data length:",len(data)
        if is_start_recv_img:
            img_local_file.write(data)
            recv_size=recv_size-len(data)
            if recv_size<=0:
                img_local_file.close()
                is_start_recv_img = False
                data = json.dumps({'device_id': "123456", 'method':'image_uploaded', 'ts':time.time()})
                client.sendall(data)
        else:
            try:
                data = json.loads(data)
            except:
                print "test_proc: recieve is not a json!"
                sys.exit(1)
            print "test_proc:recieve data:", data
            if data.has_key("method") and data['method'] == "push_image":
                recv_size = int(data['size'])
                is_start_recv_img = True
            
                img_local_file = open('./test{0}.jpg'.format(time.time()),'wb')
                print "test_proc: send data back"
                data = json.dumps({'device_id': "123456", 'method':'push_image_ready', 'ts':time.time()})
                client.sendall(data)


def recv_proc(event, ready_event, test_suit):
    global jres
    p =socket.gethostbyname(tcpc_dst_url)
    res = None
    while True:
        if config._is_debug:
            ready_event.set()
            res = test_suit.recv(1024)
        else:
            ret = wiz.loopback_tcpc(0,str(p),tcpc_dst_port)

            if ret == WIZNET_READY:
                ready_event.set()
            if ret == WIZNET_GOT_DATA:
                res = wiz.tcpc_recv(1024)
        if res is not None and len(res)>0:
            try:
                jres = json.loads(res)
                print "recv_proc:",jres
                event.set()
            except:
                print "recv_proc: recieve not json!"


def main_proc(event,ready_event, test_suit):
    global jres
    cf = config.get_instance()
    up_dict = {'device_id':cf.get_device_id(),
               'device_config_id':cf.get_device_config_id(),
               'method':'push_image'}
    dp = data_pool.get_instance()
    imgs = dp.get_imgs(10)
    ready_event.wait(5)
    if not ready_event.is_set():
        sys.exit(1)

    for img in imgs:
        up_dict['key'] = img[1]
        up_dict['size'] = get_file_size(img[2])
        up_dict['acquisition_time'] = img[0]
        if config._is_debug and test_suit is not None:
            print "main_proc:send json:", up_dict
            test_suit.send(json.dumps(up_dict))
        else:
            wiz.socket_send(json.dumps(up_dict))
        event.wait(3)
        if event.is_set() and jres is not None and  jres.has_key('method') and jres['method'] == 'push_image_ready':
            event.clear()
            f = open(img[2],'rb')
            jres = None
            chunk_size = get_file_size(img[2])
            tmp_size = 0
            if config._is_debug and test_suit is not None:
                for i in range(chunk_size/1024):
                    chunk = f.read(1024)
                    tmp_size = tmp_size + 1024
                    test_suit.send(chunk)
                chunk = f.read(1024)
                test_suit.send(chunk)
                tmp_size = tmp_size+len(chunk)
                print "main_proc: final send chunk with size:",tmp_size
            else:
                for i in range(chunk_size/1024):
                    chunk = f.read(1024) 
                    wiz.socket_send(0, chunk, len(chunk))
                chunk = f.read(1024)
                wiz.socket_send(0,chunk, len(chunk))
            event.wait(3)
            if event.is_set() and jres is not None and jres.has_key('method') and jres['method'] == 'image_uploaded':
                event.clear()
                print "main_proc:image uploaded"
                #dp.del_img(img)

if __name__ == "__main__":
    test_suit = None
    init_tcpc()
    if config._is_debug:
        test_suit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if config._is_local:
            tt = threading.Thread(target=test_proc,name="test proc")
            tt.setDaemon(True)
            tt.start()
        try:
            test_suit.connect((config._debug_ip, config._debug_port))
        except socket.error:
            print 'fail to setup socket connection'
            exit(1)
    et = threading.Event()
    rt = threading.Event()
    mp = threading.Thread(target=main_proc, args=(et,rt,test_suit), name="main proc")
    rp = threading.Thread(target=recv_proc, args=(et,rt,test_suit), name="recv proc")
    rp.setDaemon(True)
    rp.start()
    mp.start()
    mp.join()
