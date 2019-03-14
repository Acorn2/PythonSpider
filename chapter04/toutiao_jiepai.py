#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/2 16:44
software: PyCharm
description: 今日头条搜索“街拍”，进行图片爬取，目前该内容可以爬取，但是得到的json内容与实际不符
'''
import requests
from urllib.parse import urlencode
import os,json
from hashlib import md5
from multiprocessing.pool import Pool

def get_page(offet):
    params = {
        'aid':'24',
        'app_name':'web_search',
        'offset':offet,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':'20',
        'en_qc':'1',
        'cur_tab':'1',
        'from':'search_tab',
        'pd':'synthesis'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None

def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            print(item)
            if 'title' in item:
                title = item.get('title')
                images = item.get('image_list')
                for image in images:
                    data = {
                        'image': image.get('url'),
                        'title':title
                    }
                    # yield {
                    #     'image':image.get('url'),
                    #     'title':title
                    # }
#保存图片
def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path,'wb') as fw:
                    fw.write(response.content)
            else:
                print('Already Download',file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')

def main(offset):
    json = get_page(offset)
    # print(json.get('data'))
    get_images(json)
    # for item in get_images(json):
    #     print(item)
        # save_image(item)

GROUP_START = 1
GROUP_END = 20

if __name__ == '__main__':
    # pool = Pool()
    # groups = ([x * 20 for x in range(GROUP_START,GROUP_END+1)])
    # pool.map(main,groups)
    # pool.close()
    # pool.join()
    main(1)
