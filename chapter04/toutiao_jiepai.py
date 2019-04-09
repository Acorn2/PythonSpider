#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/2 16:44
software: PyCharm
description: 今日头条搜索“街拍”，进行图片爬取，也可搜索别的关键词，目前只是爬取部分缩略图，感兴趣的可以继续往下爬取
'''
import requests
from urllib.parse import urlencode
import os, json
from hashlib import md5
from multiprocessing.pool import Pool
from functools import partial
import time


def get_page(offet, keywords):
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offet,
        'format': 'json',
        'keyword': keywords,
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }

    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(params)
    print(url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None


def get_images(json):
    page_datas = []
    if json.get('data'):
        print(len(json.get('data')))
        for item in json.get('data'):
            if item.get('cell_type') is not None:
                continue
            if 'emphasized' in item:
                title = item.get('emphasized').get('title')
                title = str(title).replace('<em>', '').replace('</em>', '')
                image_urls = []
                for image in item.get('image_list'):
                    image_urls.append(image.get('url'))
                data = {
                    'article_url': item.get('article_url'),  # 详细网址
                    'title': title,  # 标题
                    'image_urls': image_urls  # 缩略图网址
                }
                page_datas.append(data)
    return page_datas


# 对于标题进行标准替换
def replace_char(x):
    replaceTab = [('/', ''), ('\\', ''), (':', ''), ('?', ' '), ('*', ''), ('"', ''), ('<', ''), ('>', ''), ('|', '')]
    for t in replaceTab:
        x = x.replace(t[0], t[1])
    return x.strip()


# 保存图片
def save_image(title_path, url):
    if not os.path.exists(title_path):
        os.mkdir(title_path)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_path = md5(response.content).hexdigest()
            image_cl = 'jpg'
            file_path = '{title_path}/{image_path}.{image_cl}'.format(title_path=title_path, image_path=image_path,
                                                                      image_cl=image_cl)
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as fw:
                    fw.write(response.content)
            else:
                print('Already Download', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')


def main(offset, keywords):
    json = get_page(offset, keywords)
    image_datas = get_images(json)

    if not os.path.exists('toutiao'):
        os.mkdir('toutiao')

    for image in image_datas:
        title_path = 'toutiao' + '/' + replace_char(str(image.get('title')))
        for url in image.get('image_urls'):
            save_image(title_path, url)
    # for item in get_images(json):
    #     print(item)
    # save_image(item)


GROUP_START = 0
GROUP_END = 1

if __name__ == '__main__':
    stime = time.time()
    keywords = str(input("请输入想要查询的关键词：\n"))

    pool = Pool()
    partial_work = partial(main, keywords=keywords)
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END)])
    pool.map(partial_work, groups)
    pool.close()
    pool.join()
    # main(0,keywords)

    print("爬取结束，内容写入完毕！")
    etime = time.time()
    print("图片下载共耗时%s s" % (str(etime - stime)))
