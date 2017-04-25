#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/10
"""
import conclude
import serial
import struct
from random import randint
from commons.conf import config
import time

class uart_controller(object):
    start_pos = 3
    instance = None
    uart_sign = '/dev/ttyAMA0'
    uart_baud = 9600
    uart_timeout =1 
    
    #ad_start_pos = [{ 'start_pos':0x10, 'value_num':4},
    #                { 'start_pos':0x20, 'value_num':4},
    #                { 'start_pos':0x30, 'value_num':4}]
    
    ad_start_pos = [{ 'start_pos':0x10, 'value_num':4,'frame_num':3},]
    ad_format_count = 12
    ad_format_index = [[2.2261, 49.248],
                       [2.2557, 69.179],
                       [2.2222, 57.902],
                       [2.2212, 67.187],
                       [2.1706, 82.135],
                       [2.221, 70.634],
                       [2.2213,79.606],
                       [2.1845, 93.705],
                       [2.2072, 61.486],
                       [3.6177, 80.657],
                       [2.2378, 79.651],
                       [2.2314, 78.603]]
    def __init__(self):
        self.ser = serial.Serial(self.uart_sign, self.uart_baud, timeout=self.uart_timeout)
        #self.ser = serial.Serial(self.uart_sign, self.uart_baud)

    @staticmethod
    def get_instance():
        if uart_controller.instance == None:
            uart_controller.instance = uart_controller()
        return uart_controller.instance

    def uart_open(self):
        if not self.ser.isOpen():
            self.ser.open()

    def uart_close(self):
        if self.ser.isOpen():
            self.ser.close()

    @classmethod
    def int_to_hex_string(cls, v):
        s = hex(v)
        if len(s[2::])%2==1:
            s ="0" +s[2::]
            return s
        return s[2::]

    @classmethod
    def int_array_to_string(cls, arr):
        if len(arr) == 0:
            return ""
        s=""
        if not isinstance(arr[0], int):
            return
        for item in arr:
            s+=cls.int_to_hex_string(item)
        return s

    @classmethod
    def CRC16(cls, data):
        CRC16Lo = 0xff
        CRC16Hi = 0xFF
        CL = 0x01
        CH = 0xA0
        for i in range(len(data)):
            CRC16Lo ^= data[i]
            for Flag in range(8):
                SaveHi = CRC16Hi
                SaveLo = CRC16Lo
                CRC16Hi >>= 1
                CRC16Lo >>= 1
                if (SaveHi & 0x01) == 0x01:
                    CRC16Lo  |=0x80
                if (SaveLo & 0x01) == 0x01:
                    CRC16Hi  ^= CH
                    CRC16Lo  ^= CL
        return (CRC16Hi<<8)|CRC16Lo

    @classmethod
    def form_read_command(cls, addr, code, start_pos, value_num):
        data=[]
        data.append(addr)
        data.append(code)
        data.append(start_pos/256)
        data.append(start_pos%256)
        data.append(value_num/256)
        data.append(value_num%256)
        crc =cls.CRC16(data)
        data.append(crc%256)
        data.append(crc/256)
        return data

    @classmethod
    def bytes_to_ushort(cls, buf, offset):
        return struct.unpack_from(">H", buf, offset)[0]
    @classmethod
    def bytes_to_int(cls, buf, offset):
        return struct.unpack_from(">B", buf, offset)[0]

    def read_by_modbus(self, start_pos, value_num):
        command = uart_controller.form_read_command(1, 3, start_pos, value_num)
        print command
        hexer = uart_controller.int_array_to_string(command).decode("hex")
        if False:
            res_int = self.construct_debug_data()
            ans = uart_controller.int_array_to_string(res_int).decode("hex")
        else:
            self.ser.write(hexer)
            ans = self.ser.readall()
        return ans
    def construct_debug_data(self):
        res_int = [1,3,4]
        for i in range(10):
            res_int.append(randint(0,255))
        return res_int
    def construct_single_ad(self, i, value):
        if i<self.ad_format_count:
            print value,self.ad_format_index[i][0],self.ad_format_index[i][1]
            current = (value*self.ad_format_index[i][0]-self.ad_format_index[i][1])*12.0/4096.0
        else:
            current = (value-150.0)/4096.0*3*1.757/249*1000
        return current
    def read_ad_values(self):
        res = []
        for conf in self.ad_start_pos:
            ans = self.read_by_modbus(conf['start_pos'], conf['value_num'])
            print len(ans)
            test_ans = []
            for k in range(len(ans)):
                 test_ans.append(uart_controller.bytes_to_int(ans,k))
            print test_ans
            try:
                for j in range(conf['frame_num']):
                    for i in range(conf['value_num']):
                        iv = uart_controller.bytes_to_ushort(ans,j*13+self.start_pos+i*2)
                        iv = self.construct_single_ad(i+j*4, iv)
                        res.append(iv)
            except Exception as e:
                print e,res

        return res


if __name__ == "__main__":
    ut = uart_controller.get_instance()
    ut.uart_open()
    rtt = ut.read_ad_values()
    print "read res:", rtt
