#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/1 10:55
software: PyCharm
description: 
'''

'''part1'''
import requests

# r = requests.get('https://www.baidu.com/')
# print(type(r),r.status_code)

'''part2'''

data = {
    'name':'germey',
    'age':22
}
# r = requests.get('http://www.httpbin.org/get',params=data)
# print(r.text)

'''part3抓取网页'''
import re

headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
# r = requests.get('https://www.zhihu.com/explore',headers=headers)
# pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>',re.S)
# titles = re.findall(pattern,r.text)
# for item in titles:
#     print(str(item).replace('\n',''))
# print(r.text)

'''part4二进制数据
图片、音频、视频这些文件本质上都是由二进制码组成的，由于有特定的保存格式和对应的解析方式，我们才可以看到这些形形色色的多媒体。所以，想要抓取它们，就要拿到它们的二进制码。
'''

# r = requests.get("https://github.com/favicon.ico")
# with open('favicon.ico','wb') as f:
#     f.write(r.content)

'''part5 post请求'''

r = requests.post('http://httpbin.org/post',data=data)
print(r.text)