#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/1 14:06
software: PyCharm
description: 
'''
'''part1文件上传'''

import requests

# files = {'file':open('favicon.ico','rb')}
# r = requests.post("http://httpbin.org/post",files=files)
# print(r.text)

'''part2,利用知乎登录cookie实现再登录，暂不可行'''

# headers = {
#     'Cookie':'_xsrf=Xx0dcM38E8yqa3alxpZ0QZTaEfa8tmUU; _zap=ed30b674-6998-483c-853c-8f2ab942e06f; d_c0="ADAnr1J0OA6PTg1-UkjjK3YtO5zcHINYorE=|1537086758"; __gads=ID=de8eac25f1a4abaa:T=1541481952:S=ALNI_MbWYea2M5ZXOATBxETxV7Bvk-nfhA; __utmv=51854390.100-1|2=registration_date=20151130=1^3=entry_date=20151130=1; __utmz=51854390.1547081225.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/271643290/answer/525019532; tst=h; q_c1=f46b5d2e9725464abe9456df21d988d0|1551418770000|1537146039000; __utmc=51854390; tgw_l7_route=116a747939468d99065d12a386ab1c5f; __utma=51854390.1761444407.1543492286.1551418795.1551420816.4; __utmb=51854390.0.10.1551420816; capsion_ticket="2|1:0|10:1551421467|14:capsion_ticket|44:MDZiMjEzZGQ2YWU1NDM0ODg0MTQyNzdlNjkwZDU4ZTA=|4b6713f3a18a448473e3e8457875059ab42171ad41cfd592b495f41a88deef64"; z_c0="2|1:0|10:1551421489|4:z_c0|92:Mi4xMm94V0FnQUFBQUFBTUNldlVuUTREaVlBQUFCZ0FsVk5NUjVtWFFEWUptQmpIQVBUZjE2Z1QzODh2S0ZaZ0RXeWJ3|b077f3da157c0655659b041b7f5d58445f87c989c9ad345687b03d9aec3413be"',
#     'Host':'www.zhihu.com',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
# }
#
# r = requests.get('https://www.zhihu.com',headers=headers)
# print(r.text)

'''part3 会话维持'''

s = requests.Session()
# requests.get('http://httpbin.org/cookies/set/number/123456789')
s.get('http://httpbin.org/cookies/set/number/123456789')
r = s.get('http://httpbin.org/cookies')
print(r.text)