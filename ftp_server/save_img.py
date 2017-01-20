#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/12
"""
import conclude
import sys,os
import time
from commons.data_pool import data_pool

def get_Img_key(filepath):
    return "Img1"

if __name__ == "__main__":
    if len(sys.argv)>1 and os.path.exists(sys.argv[1]):
        dp = data_pool.get_instance()
        img_path = sys.argv[1]
        dp.save_img(int(time.time()),get_Img_key(img_path), img_path)
        dp.close_all()
        print dp.get_imgs(6)

