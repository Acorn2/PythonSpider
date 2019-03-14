#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/11 13:42
software: PyCharm
description: 糗事百科热图爬取
'''

import requests,re
import time,os
from hashlib import md5

def getPage(myurl):
    # myurl = "http://m.qiushibaike.com/hot/page/" + page
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }
    try:
        res = requests.get(myurl, headers=headers)
        if res.status_code == 200:
            return res.text
        else:
            return None
    except requests.ConnectionError:
        return None

def getPhoto(content):
    pattern = re.compile('<div.*?class="thumb">.*?<img.*?src="(.*?)".*?</div>',re.S)
    results = re.findall(pattern,content)
    return results

def save_image(pUrl):
    if not os.path.exists("qiushi_photo"):
        os.mkdir("qiushi_photo")
    try:
        response = requests.get(pUrl)
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format("qiushi_photo", md5(response.content).hexdigest(), 'jpg')#图片的名称可以使用其内容的MD5值，这样可以去除重复。
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as fw:
                    fw.write(response.content)
            else:
                print('Already Download', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')

if __name__ == '__main__':
    url = "https://www.qiushibaike.com/imgrank/page/"
    print("糗事百科热图爬取开始......")
    for i in range(1,2):
        url += str(i)
        content = getPage(url)
        results = getPhoto(content)
        for item in results:
            purl = "http:"+item
            save_image(purl)
    print("图片爬取结束.")

