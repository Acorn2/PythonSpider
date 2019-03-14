#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/12 17:17
software: PyCharm
description: 淘宝MM信息爬取
借鉴网址：https://blog.csdn.net/xiaoduan_/article/details/80835220
'''

import requests,re
import json,os
from urllib.parse import urlencode
from urllib import parse
from pymongo import MongoClient
from hashlib import md5
import time

client = MongoClient()
db = client.learnTest
#指定集合
collection = db.taobaoMM

class Taobao_MM:
    def __init__(self):
        # self.siteUrl = "https://v.taobao.com/v/content/live?spm=a21xh.11312869.fastEntry.10.75a8627fx8co5M&catetype=704"
        #使用该网址爬取的内容，因为返回值不能直接通过.json()转换为json格式，所以需要对返回内容处理；经测试，下面那个网址更简洁，而且可以直接返回json数据
        # self.siteUrl = "https://v.taobao.com/micromission/req/selectCreatorV3.do?cateType=704&currentPage=2&_ksTS=1552436669757_87&callback=jsonp88&&_output_charset=UTF-8&_input_charset=UTF-8"
        self.siteUrl = "https://v.taobao.com/micromission/req/selectCreatorV3.do?cateType=704"#淘女郎爬取入口
        self.datas = []#淘女郎爬取信息

    # 获取索引页面的内容
    def get_page(self,page):
        params = {
            'currentPage' : page
        }
        url = self.siteUrl + urlencode(params)
        # 设置用于访问的请求头
        headers = {
            'accept':'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.9',
            'referer':'https://v.taobao.com/v/content/live?catetype=704&from=taonvlang',
            'cookie': '_cc_=VT5L2FSpdA%3D%3D; cna=X+/vE/XpfxICAXWQe23tejwg; enc=P2kAgh3gqXelcU9LUtCrHCcdh3SKPopx9ss9PwlMBgapGSmvuFDGsg1%2BPIuIUJh%2B%2B11CSPDRGtRsiBy%2F9N1l2A%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; t=64b9616387a132e8abbc859a142d0ec4; tg=0; thw=cn; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; JSESSIONID=70FDC83B5D4EC89B5AB9DCEC75C2AB27; v=0; cookie2=139526390c3fef986de147b346c89f37; _tb_token_=55ee7e3e61ee; uc1=cookie14=UoTZ5iF3DBhZLg%3D%3D; isg=BF5e5jItjgGp7t2UOZ2VZu5vr_RgtwkpmUebFAjnpKE0K_8FcaxpqLaNI3eCMRqx',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()         
        except requests.ConnectionError:
            return None

    # 获取索引界面所有MM的信息，list格式
    def get_contents(self,json):
        result = json.get('data')
        if result:
            if result.get('result'):
                for item in result.get('result'):
                    data = {
                        'name':item.get('nick'),
                        'homeUrl':item.get('homeUrl'),
                        'fansCount':item.get('fansCount')
                    }
                    self.datas.append(data)

    # 获取MM个人详情页面
    def get_detalPage(self,infoUrl):
        url = "https://v.taobao.com/micromission/daren/daren_main_portalv3.do?"

        userId = str(parse.urlparse(infoUrl).query).split('&')[0].split('=')[1]#取出每个MM专属的页面id

        params = {
            'userId': userId
        }
        url = url + urlencode(params)
        headers = {
            'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': infoUrl,
            'cookie': '_cc_=VT5L2FSpdA%3D%3D; cna=X+/vE/XpfxICAXWQe23tejwg; enc=P2kAgh3gqXelcU9LUtCrHCcdh3SKPopx9ss9PwlMBgapGSmvuFDGsg1%2BPIuIUJh%2B%2B11CSPDRGtRsiBy%2F9N1l2A%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; t=64b9616387a132e8abbc859a142d0ec4; tg=0; thw=cn; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; JSESSIONID=70FDC83B5D4EC89B5AB9DCEC75C2AB27; v=0; cookie2=139526390c3fef986de147b346c89f37; _tb_token_=55ee7e3e61ee; uc1=cookie14=UoTZ5iF3DBhZLg%3D%3D; isg=BF5e5jItjgGp7t2UOZ2VZu5vr_RgtwkpmUebFAjnpKE0K_8FcaxpqLaNI3eCMRqx',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
        except requests.ConnectionError:
            return None

    #获取每个MM页面的信息，包括名称，个人描述，展示图等
    def get_detalMes(self,json_data):
        result = json_data.get('data')
        contents = []
        if result:
            #获取个人描述
            desc = json.loads(result.get('desc'))
            blocks = desc.get('blocks')
            for item in blocks:
                text = item.get('text')
                if text.strip():
                    contents.append(text)
            #获取个人详细页面中的图片展示，目前该页面没有相册，所以爬取的图片不多，同时，我们根据个人描述进行判断，对于
            #夫妻类的图片进行剔除爬取
            entityMap = desc.get('entityMap')
            urls_data = []
            for i in range(len(entityMap)):
                url = entityMap.get(str(i)).get('data').get('url')
                if url == None:
                    url = entityMap.get(str(i)).get('data').get('coverUrl')
                if "夫妻" not in "".join(contents):
                    urls_data.append(url)

            data = {
                'name': result.get('darenNick'),  # 用户名
                'city': result.get('city'),  # 居住地
                'area': result.get('area'),  # 服务类型
                'icon_url': result.get('picUrl'),  # 获取个人头像地址
                'content':contents,#个人描述
                'photo_urls':urls_data#展示图
            }
        return data

    #保存MM各自页面的展示图
    def save_image(self,name,url):
        file = '{0}/{1}'.format("taobaoMM",name)
        if not os.path.exists(file):
            os.mkdir(file)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                file_path = '{0}/{1}.{2}'.format(file, md5(response.content).hexdigest(), 'jpg')
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as fw:
                        fw.write(response.content)
                        print("正在悄悄保存她的一张图片为{0}".format(file_path))
                else:
                    print('Already Download', file_path)
        except requests.ConnectionError:
            print('Failed to Save Image')

    def save_pageInfo(self,datas):
        if not os.path.exists("taobaoMM"):
            os.mkdir('taobaoMM')
        for dt in datas:
            if dt["photo_urls"]:
                print("***********发现一位模特,名字叫{0},她在{1}**************".format(dt["name"],dt["city"]))
                for url in dt["photo_urls"]:
                    self.save_image(dt['name'], url)
                print("发现{0}共有{1}张图片".format(dt["name"],str(len(dt["photo_urls"]))))


    def start(self):
        print("开始爬取淘宝MM图片......")
        for i in range(1,2):
            text = self.get_page(i)
            self.get_contents(text)
            time.sleep(1)
        print(len(self.datas))

        #将网页检索的所有MM信息存放到mongodb中
        # try:
        #     for item in self.datas:
        #         collection.insert_one(item)
        # except Exception as e:
        #     print(e)
        # print("爬取的内容已经写入到mongodb中！")
        # text = self.get_detalPage(self.datas[3]["homeUrl"])
        # print(text)
        # data = self.get_detalMes(text)
        all_datas = []
        for item in self.datas:
            text = self.get_detalPage(item["homeUrl"])
            data = self.get_detalMes(text)
            all_datas.append(data)

        self.save_pageInfo(all_datas)
        print("爬取结束！")


if __name__ == '__main__':
    model = Taobao_MM()
    model.start()
