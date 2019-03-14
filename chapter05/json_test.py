#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/3 15:32
software: PyCharm
description: dumps和loads是在内存中转换（python对象和json字符串之间的转换），而dump和load则是对应于文件的处理。
出现这个错误的原因是自己用了loads方法去将json文件转换为python对象，而正确的应该是使用load方法。
'''
import json

with open('taobao.json', 'rb') as f:
    cookies = json.load(f)
    for item in cookies:
        print(item)
    print(cookies)