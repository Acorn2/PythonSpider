#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/3 16:36
software: PyCharm
description: 学习加密使用
'''

from hashlib import md5
from urllib.parse import quote

name = "xNby9pa82a7"
print(quote(name))
print(md5(name.encode('utf-8')).hexdigest())