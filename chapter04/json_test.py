#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/2 10:14
software: PyCharm
description: 
'''
import json

data = [{
    'name': 'Bob',
    'gender': 'male',
    'birthday': '1992-10-18'
},{
    'name': '李四',
    'gender': 'male',
    'birthday': '1992-10-18'
}
]

with open('djata.json','w',encoding='utf-8') as f:
    f.write(json.dumps(data,indent=2,ensure_ascii=False))#代表缩进字符个数,输出内容中文编码