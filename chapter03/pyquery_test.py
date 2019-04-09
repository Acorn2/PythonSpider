#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/2 9:24
software: PyCharm
description: 
'''

'''part1'''

html = '''
<div>
    <ul>
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''

from pyquery import PyQuery as pq

# doc = pq(html)
# print(doc('li'))

'''part2'''
import requests

# doc1 = pq(url='http://cuiqingcai.com')
# print(doc1('title'))
# doc2 = pq(requests.get('http://cuiqingcai.com').text)
# print(doc2('title'))

'''part3'''

html = '''
<div id="container">
    <ul class="list">
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''
doc = pq(html)
# print(doc('#container .list li'))
items = doc('.list')
lis = items.find('li')
print(lis)
print(items.children())
print(doc('.item'))


'''part4'''

doc = pq(html)
#标签不完全一致
items = doc('.billboard-songs .table-container .odd').items()
odd_data = []
for item in items:
    song = {
        'index': item.find('.em.index').text(),
        'name': item.find('.song-name').text(),
        'url' : 'https://www.xiami.com'+item.find('.song-name > a ').attr('href'),
        'singer': item.find('.singers').text(),
        'time': item.find('.duration-container .duration ').text()
    }