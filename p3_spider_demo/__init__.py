#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/3 16:36
software: PyCharm
description: 
'''

from hashlib import md5

name = "中文"
print(md5(name.encode('utf-8')).hexdigest())