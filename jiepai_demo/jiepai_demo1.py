#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/13 20:07
software: PyCharm
description: 爬取街拍网站图片
http://www.1jiepai.com/forum.php?page=2
'''

import requests,re
import os,time
from hashlib import md5

#根据页号爬取每一页的内容
def get_text(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError:
        return None

#针对爬取的页面内容进行提取，主要是图片详细页面地址，图片url，以及图片主题
def get_photos_urls(text):
    page_datas = []
    # pattern = re.compile('<div.*?class="scitem.*?<a.*?class="simage".*?href="(.*?)".*?<img.*?src="(.*?)".*?<div.*?class="simgh">.*?<h3>.*?'
    #                      '<a.*?class="simgtitle".*?>(.*?)</a>.*?</div>',re.S)

    pattern = re.compile(
        '<div.*?class="scitem.*?<a.*?class="simage".*?href="(.*?)".*?<img.*?src="(.*?)".*?<div.*?class="simgh">.*?<h2>.*?'
        '<a.*?class="simgtitle".*?>(.*?)</a>.*?</div>', re.S)#爬取精品视频

    results = re.findall(pattern,text)
    for item in results:
        data = {
            'detalUrl':item[0],
            'pUrl':item[1],#缩略图
            'title':item[2]
        }
        page_datas.append(data)
    return page_datas

#由于上个方法中获取的图片url下载下来的只是缩略图，所以我们根据图片详细网址爬取大图
def get_page_photo(text):
    urls = []
    pattern = re.compile(
        '<div.*?class="mbn.*?<img.*?zoomfile="(.*?)".*?</div>', re.S)

    results = re.findall(pattern, text)#页面基本都只显示一张图片，其他收费

    for item in results:
        urls.append(item)
    return urls##爬取精品视频
    # return results[0]

#根据图片url下载图片
def save_photo(pUrl):
    if not os.path.exists("jiepai_1"):
        os.mkdir('jiepai_1')

    try:
        response = requests.get(pUrl)
        if response.status_code == 200:
            file_path = "{0}/{1}.{2}".format("jiepai_1",md5(response.content).hexdigest(),"jpg")
            if not os.path.exists(file_path):
                with open(file_path,'wb') as fw:
                    fw.write(response.content)
            else:
                print('Already Download',file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')

if __name__ == '__main__':
    stime = time.time()
    print("开始爬取街拍网站的图片........")
    all_datas = []
    all_photo_urls = []
    for i in range(1,10):
        print("正在爬取第{0}页的图片信息".format(str(i)))
        # url = "http://www.1jiepai.com/forum.php?page=" + str(i)#这是街拍网站图片的网址
        #街拍网站精品视频部分也有图片，可以爬取，爬取程序一样
        url = "http://www.1jiepai.com/forum-36-"+str(i)+".html"##爬取精品视频
        text = get_text(url)
        page_datas = get_photos_urls(text)

        for item in page_datas:
            detalUrl = item['detalUrl']
            text = get_text(detalUrl)
            pUrl = get_page_photo(text)
            # all_photo_urls.append(pUrl)
            all_photo_urls.extend(pUrl)

        print("第{0}页共爬取了{1}张图片".format(str(i), str(len(page_datas))))
        # all_datas.extend(page_datas)
        time.sleep(1)

    print("图片爬取结束，开始下载......")
    # for item in all_datas:
    #     pUrl = item["pUrl"]
    #     save_photo(pUrl)
    #

    for pUrl in all_photo_urls:
        save_photo(pUrl)
    print("图片下载结束，快去欣赏吧！")
    etime = time.time()

    print("图片下载共耗时%s s" %(str(etime-stime)))