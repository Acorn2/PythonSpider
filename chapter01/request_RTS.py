#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/2/28 15:38
software: PyCharm
description: urllib.request之发送请求
'''
import urllib.request
'''part1'''
# response = urllib.request.urlopen('https://www.python.org')
# response = urllib.request.urlopen('https://www.baidu.com')
# print(response.read().decode('utf-8'))
# print(response.status)

'''part2'''
import urllib.parse

# data = bytes(urllib.parse.urlencode({'word':'hello','name':'hhhhr'}),encoding='utf8')
# response = urllib.request.urlopen('http://httpbin.org/post',data=data)
# print(response.read().decode('utf-8'))

'''part3'''
import socket
import urllib.error

# try:
#     response = urllib.request.urlopen('http://httpbin.org/get',timeout=0.1)
# except urllib.error.URLError as e:
#     if isinstance(e.reason,socket.timeout):
#         print("time out")

'''part4'''

# request = urllib.request.Request('https://baidu.com')
# response = urllib.request.urlopen(request)
# print(response.read().decode('utf-8'))

'''part5'''
from urllib import request,parse

# url = 'http://httpbin.org/post'
# headers = {
#     'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
#     'Host': 'httpbin.org'
# }
# dict = {'word':'hello','name':'hhhhr'}
#
# data = bytes(parse.urlencode(dict),encoding='utf-8')
# req = request.Request(url=url,headers=headers,data=data,method='POST')
# res = request.urlopen(req)
# print(res.read().decode('utf-8'))

'''part6当遇到登录界面需要用户名和密码时
有些网站在打开时就会弹出提示框，直接提示你输入用户名和密码，验证成功后才能查看页面
测试代码暂不可行
'''

from urllib.request import HTTPPasswordMgrWithDefaultRealm,HTTPBasicAuthHandler,build_opener
from urllib.error import URLError

# username = "username"
# password = 'password'
# url = 'http://localhosr:5000/'
#
# p = HTTPPasswordMgrWithDefaultRealm()
# p.add_password(None,url,username,password)
# auth_handler = HTTPBasicAuthHandler(p)
# opener = build_opener(auth_handler)
#
# try:
#     result = opener.open(url)
#     html = result.read().decode('utf-8')
#     print(html)
# except URLError as e:
#     print(e.reason)

'''part7
添加代理,测试代码暂不可行
'''

from urllib.request import ProxyHandler,build_opener

# proxy_handler = ProxyHandler({
# 'http': 'http://127.0.0.1:9743',
#     'https': 'https://127.0.0.1:9743'
# })
#
# opener = build_opener(proxy_handler)
# try:
#     res = opener.open('https://www.baidu.com')
#     print(res.read().decode('utf-8'))
# except URLError as e:
#     print(e.reason)

'''part8 cookie'''
import http.cookiejar

# # cookie = http.cookiejar.CookieJar()
# filename = 'cookie.txt'
# cookie = http.cookiejar.MozillaCookieJar(filename)#在生成文件时会用到
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# res = opener.open('http://www.baidu.com')
# # for item in cookie:
# #     print(item.name+"="+item.value)
# cookie.save(ignore_discard=True,ignore_expires=True)
