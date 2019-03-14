#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/12 16:18
software: PyCharm
description: 利用百度搜索接口，编写url采集器
'''
import requests
from bs4 import BeautifulSoup

def get_text(offset):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }

    url = "https://www.baidu.com/s?wd=inurl:/dede/login.php?&pn=" + str(offset)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError:
        return None

if __name__ == '__main__':


    for i in range(0,100,10):
        # url = "https://www.baidu.com/s?wd=inurl:/dede/login.php?&pn=0"
        text = get_text(i)
        soup = BeautifulSoup(text,'lxml')
        url_list = soup.select('.t > a')
        for url in url_list:
            real_url = url['href']
            print(real_url)