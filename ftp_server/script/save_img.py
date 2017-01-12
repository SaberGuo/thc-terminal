#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  @author: xiao guo
  @contact: guoxiao@buaa.edu.cn
  @date: 2017/1/12
"""

import sys,os
import time
from commons.data_pool import data_pool

if __name__ == "__main__":
    if len(sys.argv)>2 and os.path.exists(sys.argv[1]):
        dp = data_pool.get_instance()
        img_path = sys.argv[1]
        dp.save_img(time.time(), img_path)

