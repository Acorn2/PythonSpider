#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/2 8:44
software: PyCharm
description: 
'''

'''part1'''

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

from bs4 import BeautifulSoup

# soup = BeautifulSoup(html,'lxml')
# print(soup.title)
# print(type(soup.title))
# print(soup.title.string)
# print(soup.head)
# print(soup.p)

'''part2'''

html='''
<div class="panel">
    <div class="panel-heading">
        <h4>Hello</h4>
    </div>
    <div class="panel-body">
        <ul class="list" id="list-1">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
            <li class="element">Jay</li>
        </ul>
        <ul class="list list-small" id="list-2">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
        </ul>
    </div>
</div>
'''

# soup = BeautifulSoup(html,'lxml')
# print(soup.find_all(name='ul'))
# print(type(soup.find_all(name='ul')[0]))
# for ul in soup.find_all(name='ul'):
#     for li in ul.find_all(name='li'):
#         print(li.string)

'''part3'''

# soup = BeautifulSoup(html,'lxml')
# print(soup.find_all(attrs={'id':'list-1'}))

'''part4'''
import re

# soup = BeautifulSoup(html,'lxml')
# print(soup.find_all(text=re.compile('link')))

'''part5'''

soup = BeautifulSoup(html,'lxml')
print(soup.select('.panel .panel-heading'))
print(soup.select('ul li'))
print(soup.select('#list-2 .element'))


'''part6'''

for li in soup.select('li'):
    print('Get Text:',li.get_text())
    print('String:',li.string)