#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/1 10:03
software: PyCharm
description: 
'''

'''part1'''

from urllib.parse import urlparse

# result = urlparse('http://www.baidu.com/index.html;user?id=5#comment')
# print(type(result),result)


'''part2'''
from urllib.parse import urlsplit

# result = urlsplit('http://www.baidu.com/index.html;user?id=5#comment')
# print(result)

'''part3'''

from urllib.parse import urlencode

params = {
    'name':'germey',
    'age':22
}
base_url = 'http://www.baidu.com?'
url = base_url + urlencode(params)
print(url)

'''part4'''
from urllib.parse import parse_qs

query = 'name=germey&age=22'
print(parse_qs(query))

'''part5将内容转化为URL编码的格式'''
from urllib.parse import quote

keyword = '壁纸'
url = 'https://www.baidu.com/s?wd='+quote(keyword)
print(url)

'''part6'''