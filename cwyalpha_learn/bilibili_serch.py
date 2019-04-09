#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/17 20:02
software: PyCharm
description: 
'''

import requests
from pyquery import PyQuery as pq
from urllib.parse import urlencode

class Bilibili:
    def __init__(self,keywords):
        self.keywords = keywords
        self.page = 1
        self.data = []

    def get_page(self):
        params = {
            'keyword' : self.keywords,
            'from_source' : 'banner_search',
            'page' : self.page
        }
        url = 'https://search.bilibili.com/all?' + urlencode(params)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)

            response.encoding = response.apparent_encoding
            if 200 == response.status_code:
                return response.text
        except requests.ConnectionError as e:
            return None

    def deal_page(self):
        html = self.get_page()
        # print(html)
        doc = pq(html)
        items = doc('.result-wrap.clearfix .video.matrix ').items()

        for item in items:
            result = {
                'vedio_url' : 'https:' + item.find('.img-anchor').attr('href'),
                # 'icon_url' : item.find('.lazy-img').text(),
                'duration' : item.find('.so-imgTag_rb').text(),
                'title' : item.find('.info .title').text(),
                'watch_num' : item.find('.watch-num').text(),
                'barrage' : item.find('.so-icon.hide').text(),
                'time' : item.find('.so-icon.time').text(),
                'up_name' : item.find('.up-name').text(),
                'up_url' : 'https:' + item.find('.up-name').attr('href')
            }
            print(result)

    def start(self):
        self.deal_page()


if __name__ == '__main__':
    bb = Bilibili('Python')
    bb.start()