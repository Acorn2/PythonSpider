#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/1 15:08
software: PyCharm
description: 
'''
'''part1
在做匹配的时候，字符串中间尽量使用非贪婪匹配，也就是用.*?来代替.*，以免出现匹配结果缺失的情况。
'''
import re

# content = 'Hello 1234567 World_This is a Regex Demo'
# result1 = re.match('^He.*(\d+).*Demo$',content)#贪婪匹配
# result2 = re.match('^He.*?(\d+).*Demo$',content)#非贪婪匹配
# print(result1)
# print(result1.group(1))
# print(result2)
# print(result2.group(1))

'''part2
需要注意，如果匹配的结果在字符串结尾，.*?就有可能匹配不到任何内容了，因为它会匹配尽可能少的字符。
'''

# content = 'http://weibo.com/comment/kEraCN'
# result1 = re.match('http.*?comment/(.*?)',content)
# result2 = re.match('http.*?comment/(.*)',content)
# print('result1',result1.group(1))
# print('result2',result2.group(1))

'''part3
\.匹配的是除换行符之外的任意字符，当遇到换行符时，.*?就不能匹配了，所以导致匹配失败。
这里只需加一个修饰符re.S，即可修正这个错误：
'''
# content = '''Hello 1234567 World_This
# is a Regex Demo
# '''
#
# result = re.match('^He.*?(\d+).*?Demo$',content,re.S)
# print(result.group(1))

'''part4 转义匹配'''

# content = '(百度)www.baidu.com'
# result = re.match('\(百度\)www\.baidu\.com',content)
# print(result)

'''part5 
match()方法是从字符串的开头开始匹配的，一旦开头不匹配，那么整个匹配就失败了。
'''
# content = 'Extra stings Hello 1234567 World_This is a Regex Demo Extra stings'
# # result = re.match('Hello.*?(\d+).*?Demo',content)
# result = re.search('Hello.*?(\d+).*?Demo',content)
# print(result)
# print(result.group(1))

'''part6'''
html = '''<div id="songs-list">
    <h2 class="title">经典老歌</h2>
    <p class="introduction">
        经典老歌列表
    </p>
    <ul id="list" class="list-group">
        <li data-view="2">一路上有你</li>
        <li data-view="7">
            <a href="/2.mp3" singer="任贤齐">沧海一声笑</a>
        </li>
        <li data-view="4" class="active">
            <a href="/3.mp3" singer="齐秦">往事随风</a>
        </li>
        <li data-view="6"><a href="/4.mp3" singer="beyond">光辉岁月</a></li>
        <li data-view="5"><a href="/5.mp3" singer="陈慧琳">记事本</a></li>
        <li data-view="5">
            <a href="/6.mp3" singer="邓丽君"><i class="fa fa-user"></i>但愿人长久</a>
        </li>
    </ul>
</div>'''

# result = re.search('<li.*?active.*?singer="(.*?)">(.*?)</a>',html,re.S)
# if result:
#     print(result.group(1),result.group(2))

'''part7'''
# results = re.findall('<li.*?href="(.*?)".*?singer="(.*?)">(.*?)</a>',html,re.S)
# print(results)
# print(type(results))
# for i in results:
#     print(i)
#     print(i[0],i[1],i[2])

'''part8'''

# html = re.sub('<a.*?>|</a>','',html)
# print(html)
# results = re.findall('<li.*?>(.*?)</li>',html,re.S)
# for i in results:
#     print(i.strip())


'''part9'''

content1 = '2018-03-01 16:09'
pattern = re.compile('\d{2}:\d{2}')
result = re.sub(pattern,'',content1)
print(result)