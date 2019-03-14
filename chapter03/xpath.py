#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/1 20:04
software: PyCharm
description: 
'''

from lxml import etree

text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''

# html = etree.HTML(text)
# result = etree.tostring(html)
# print(result.decode('utf-8'))
# with open('test.html','w',encoding='utf-8') as f:
#     f.write(result.decode('utf-8'))

'''part2所有节点'''

# html = etree.parse('test.html',etree.HTMLParser())
# result = html.xpath('//li')
# result = html.xpath('//li/a')
# result = html.xpath('//ul//a')
# print(result)

'''part3父节点'''

# html = etree.parse('test.html',etree.HTMLParser())
# result = html.xpath('//a[@href="link4.html"]/parent::*/@class')
# print(result)

'''part4 文本获取'''
# html = etree.parse('test.html',etree.HTMLParser())
# result = html.xpath('//li[@class="item-0"]/a/text()')
# print(result)

'''part5 属性获取'''
# html = etree.parse('test.html',etree.HTMLParser())
# result = html.xpath('//li/a/@href')
# print(result)

'''part6 属性多值匹配'''

text = '''
<li class="li li-first"><a href="link.html">first item</a></li>
'''
html = etree.HTML(text)
result = html.xpath('//li[contains(@class,"li")]/a/text()')
print(result)