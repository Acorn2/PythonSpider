#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/11 16:37
software: PyCharm
description: 爬取煎蛋网图片，这里爬取的网页内容与浏览器中显示的html内容不一致，获取图片地址的时候使用BeautifulSoup最为简洁。
'''

import requests,os,time
from bs4 import BeautifulSoup
import base64
from hashlib import md5

#解决网页防爬虫和封ip
headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
    }

def getUrls(text):
    hash_list = []
    img_addr_list = []

    soup = BeautifulSoup(text,'lxml')

    data = soup.findAll('span','img-hash')
    for dd in data:
        hash_list.append(dd.string)

    for eachHashCode in hash_list:
        url = base64.b64decode(eachHashCode).decode('utf-8')
        img_addr_list.append('https:'+url)

    return img_addr_list

#保存图片
def save_image(url):
    if not os.path.exists("jiantu"):
        os.mkdir('jiantu')
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format("jiantu",md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path,'wb') as fw:
                    fw.write(response.content)
            else:
                print('Already Download',file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')

if __name__ == '__main__':
    start_time = time.time()

    print("开始爬取煎蛋网美图.....")
    all_imgUrls = []
    for i in range(1,2):
        url = 'http://jandan.net/ooxx/page-'+str(i)+'#comments'
        response = requests.get(url,headers=headers)
        # print(response.text)
        img_urls = getUrls(response.text)
        print("第{0}页共爬取{1}张图片".format(str(i),str(len(img_urls))))
        all_imgUrls.extend(img_urls)
        time.sleep(3)

    print("爬取结束，下载并保存！")
    for iurl in all_imgUrls:
        save_image(iurl)

    print("一共{}张图片下载完成，去欣赏吧！".format(len(all_imgUrls)))

    end_time= time.time()
    print("共耗时{}s".format(end_time-start_time))
