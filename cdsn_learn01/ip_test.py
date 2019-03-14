#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/12 16:10
software: PyCharm
description: 
'''

import requests,lxml
import re

try:
    res = requests.get('http://2017.ip138.com/ic.sap')
    res.encoding = res.apparent_encoding
except requests.ConnectionError:
    print("连接失败！")

print(res.text)

# print(re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",res.text))
