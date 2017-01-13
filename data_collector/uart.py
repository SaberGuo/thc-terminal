#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/10
"""

import serial
import struct
from random import randint

class uart_controller(object):
    start_pos = 3
    instance = None
    uart_sign = '/dev/ttyAMA0'
    uart_baud = 9600
    uart_timeout = 0.5
    _is_debug_ = True

    ad_start_pos = [{ 'start_pos':0x10, 'value_num':4},
                    { 'start_pos':0x20, 'value_num':4},
                    { 'start_pos':0x30, 'value_num':4}]
    def __init__(self):
        self.ser = serial.Serial(self.uart_sign, self.uart_baud, timeout=self.uart_timeout)

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
    def int_to_hex_str(cls, v):
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
    def bytes_to_ushort(buf, offset):
        return struct.unpack_from(">H", buf, offset)[0]

    def read_by_modbus(self, start_pos, value_num):
        command = uart_controller.form_read_command(1, 3, start_pos, value_num)
        hexer = uart_controller.int_array_to_string(command).decode("hex")
        if self._is_debug_:
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

    def read_ad_values(self):
        res = []
        for conf in self.ad_start_pos:
            ans = self.read_by_modbus(conf['start_pos'], conf['value_num'])
            for i in range(conf['value_num']):
                res.append(uart_controller.bytes_to_ushort(ans,self.start_pos+i*2))

        return res
