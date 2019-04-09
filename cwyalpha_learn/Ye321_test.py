#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/16 20:45
software: PyCharm
description: 
'''

import requests,re
from pyquery import PyQuery as pq
from pymongo import MongoClient
import time
import os
from hashlib import md5

client = MongoClient()
db = client.learnTest
collection = db.ye321

def get_text(url):

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'UM_distinctid=169868e76246e3-0163673abb35df-9333061-1fa400-169868e76255d1; CNZZDATA1000283933=160834316-1552736341-%7C1552736341',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }
    try:
        response = requests.get(url,headers=headers)

        response.encoding = response.apparent_encoding
        if 200 == response.status_code:
            return response.text
    except requests.ConnectionError as e:
        time.sleep(1)#一旦爬取失败，设置等待时间
        return None

def deal_text(text):
    data = []
    pattern = re.compile('<tr.*?<td.*?<a.*?href="(.*?)".*?>(.*?)</a>.*?<td.*?<a.*?href="(.*?)".*?>(.*?)</a>.*?<td.*?<font.*?>(.*?)</font>.*?'
                         '<td.*?<font.*?>(.*?)</font>.*?<td.*?<font.*?>(.*?)</font>.*?</tr>',re.S)

    results = re.findall(pattern,text)

    for item in results:
        time = item[6].strip()
        if re.match('^[0-9-]+$',time):#匹配的有错误的信息，根据发布时间进行区分
            mess = {
                'url' : 'http://www.uuzyz005.com' + item[0].strip(),#资源详细地址
                'name' : item[1].strip(),#资源名称
                'category_url': 'http://www.uuzyz005.com' + item[2].strip(),#资源分类url
                'category': item[3].strip(),#资源分类
                'area': item[4].strip(),#地区（无用信息）
                'update': item[5].strip(),#更新状态（无用）
                'time': item[6].strip()#更新时间
            }
            # print(mess)
            data.append(mess)
    return data

def get_detal_page(text):
    doc = pq(text)
    pattern = re.compile('<tbody.*?<tr.*?<td.*?<img.*?src="(.*?)".*?class="img".*?<div.*?<font.*?>(.*?)</font>.*?<font.*?>(.*?)</font>.*?<font.*?>(.*?)</font>.*?'
                         '<font.*?>(.*?)</font>.*?<font.*?>(.*?)</font>.*?<font.*?>(.*?)</font>.*?<font.*?>(.*?)</font>.*?</td>.*?</tr>.*?</tbody>'
                         '.*?<div.*?id="plist".*?<td.*?<ul.*?<li.*?<a.*?href="(.*?)".*?</a>.*?</li>.*?</ul>.*?</td>.*?</div>',re.S)
    results = re.findall(pattern,text)

    info = doc('.intro').items()#利用pyquery方法提取剧情介绍内容，方便处理文本内容

    for item in results:
        abstract = str(item[8].strip()).replace('<strong>','').replace('</strong>','').replace('<br>',' ')
        mess = {
            'photo_url': item[0].strip(),  # 资源图片地址
            'name': item[1].strip(),  # 资源名称
            'actor': item[3].strip(),  # 演员
            'category': item[5].strip(),  # 资源分类
            'area': item[6].strip(),  # 地区
            'time': item[7].strip(),  # 更新时间
            'abstract' : str(next(info).text()).replace('\n',''),#简介
            'url' : 'http://www.uuzyz005.com' + item[8].strip()#资源播放地址
        }
        print(mess)
    return mess

#根据输入的关键词进行数据匹配
def get_keywords_data(keywords,datas):
    new_data = []
    for item in datas:
        movie_name = item['name']
        actor = item['actor']
        if keywords in movie_name or keywords in actor:
            print(item)
            new_data.append(item)
    return new_data

#保存图片
def save_icon(mess,keywords):
    pUrl = mess['photo_url']

    file = '{0}/{1}'.format("Ye321", keywords)
    if not os.path.exists(file):
        os.mkdir(file)
    try:
        response = requests.get(pUrl)
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(file, md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as fw:
                    fw.write(response.content)
                    print("正在保存以“{0}”关键词搜索的资源的图片为{1}".format(keywords,file_path))
            else:
                print('Already Download', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')

#将爬取的结果存入mongodb中
def save_to_mongo(datas):
    try:
        collection.insert_many(datas)
    except Exception as e:
        print(e)

def read_mogo(keywords):
    #想sql查询那样模糊查询，可是测试之后发现模糊查询的效果不好，可能是哪里存在限制
    #创建索引，我在这里尝试失败，需要到mongodb中添加
    # collection.create_Index({'name': "text", 'actor': "text"})
    # collection.ensureIndex({'name': "text", 'actor': "text"})
    datas = []
    # results1 = collection.find({'$text': {'$search': keywords}})#返回的是生成器类型
    #
    # print(results1)
    # for item in results1:
    #     print(item)
    #     datas.append(item)

    results = collection.find()
    for item in results:
        datas.append(item)
    return datas


if __name__ == '__main__':

    print(u''
          '************你懂的资源爬取************\n'
          '0.all\n'
          '1.zhifu\n'
          '2.siwa\n'
          '3.shaofu\n'
          '4.xuesheng\n'
          '5.meitui\n'
          '6.juru\n'
          '7.meishaonv\n'
          '8.zipai')

    titles = ['','/zhifu','/siwa','/shaofu','/xuesheng','/meitui','/juru','/meishaonv','/zipai']

    # num = int(input('请输入数字：\n'))
    # titie = str(titles[num]).replace('/','') if titles[num] else '全部类型'
    # print("准备爬取主题为{0}的资源....".format(titie))
    # page_datas = []
    # for i in range(232,233):
    #     print("正在爬取第{0}页的资源....".format(str(i)))
    #     url = 'http://www.uuzyz005.com'+ str(titles[num]) +'/index-' + str(i) + '.html'#按照时间顺序进行爬取
    #     text = get_text(url)
    #     data = deal_text(text)
    #
    #     for item in data:
    #         detal_url = item['url']
    #         detal_text = get_text(detal_url)
    #         page_datas.append(get_detal_page(detal_text))
    #
    # print("一共爬取到{0}个资源".format(str(len(page_datas))))
    # print("将爬取的资源存入到mongodb中")
    # save_to_mongo(page_datas)
    # print("资源信息保存完毕！")

    keywords = str(input("根据爬取的资源，搜索影片名或演员名称:\n"))
    mongo_data = read_mogo(keywords)

    new_datas = get_keywords_data(keywords,mongo_data)

    if not os.path.exists("Ye321"):
        os.mkdir('Ye321')
    for data in new_datas:
        save_icon(data,keywords)
    print("图片下载结束！")
    # detal_text = get_text('http://www.uuzyz005.com/shaofu/931/')
    # # print(detal_text)
    # get_detal_page(detal_text)
