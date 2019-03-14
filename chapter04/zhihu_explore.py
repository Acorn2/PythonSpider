#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/2 9:53
software: PyCharm
description: 知乎上“发现”页面的“热门话题”部分，将其问题和答案统一保存成文本形式。
'''

import requests,re
from pyquery import PyQuery as pq

url = 'https://www.zhihu.com/explore'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
html = requests.get(url,headers=headers).text
doc = pq(html)
items = doc('.explore-tab .feed-item').items()
for item in items:
    question = item.find('h2').text()
    author = item.find('.author-link').text()
    content = pq(item.find('.content').html()).text()
    print(question,author,content)
    with open('zhihu.txt','a',encoding='utf-8') as f:
        f.write('\n'.join([question,author,content]))
        f.write('\n'+'*'*50+'\n')
