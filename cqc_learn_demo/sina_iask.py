#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/15 10:20
software: PyCharm
description: 抓取爱问知识人问题并保存至数据库,pyquery用起来感觉更加简单
'''
import requests,re
from pyquery import PyQuery as pq
from urllib.parse import urlencode
from pymongo import MongoClient


client = MongoClient()
db = client.learnTest
collection = db.sina_iask

def get_text(page,keywords):
    params = {
        'searchWord': keywords,
        'page': page,
        'iask_cookie':'15526189624380.4812448591083074'
    }
    #请求头的重要性，当爬取不到内容时（排除ajax的情况下），一定要仔细研究请求头，不然爬取不到任何内容。即使使用selenium也不好使
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'cookie':'SINAGLOBAL=10.22.254.22_1534986742.267637; U_TRS1=0000006c.a115496.5b7e9887.d69d3490; UOR=www.baidu.com,blog.sina.com.cn,; SGUID=1537779660926_44692152; Hm_lvt_4a6f318ce337dd0d624bc1258f28517a=1544753481; Hm_lvt_6d9dbd40938652c96621337da0d57597=1544753481; Hm_lvt_882eeb189ca009335b038a7981f54594=1544753481; SUB=_2AkMrdllUf8NxqwJRmfgUxGzlao1-ywzEieKdKqiPJRMyHRl-yD9jqlNStRB6APZ3uzFYfc94Rl63LieG_JRY1jhtOYmj; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWUBfqwAzrJBNL_Nujm7iWE; lxlrtst=1547190260_o; lxlrttp=1547190260; Hm_lvt_010cf6ff0772556e078700414dd56e55=1547296673; ULV=1550145835211:5:1:1::1547191351685; JSESSIONID=2db01cba-47a9-4d52-a244-08a4a5d82440; UM_distinctid=1697f167a50303-0b89535383b7c8-9333061-1fa400-1697f167a51422; CNZZDATA1262400696=2088269660-1552615370-%7C1552615370; Hm_lvt_ad29670c49e093f8aa6cbb0f672c1a81=1552615928; Hm_lvt_ce3365747bc6e46f69b1506dbb7b55ba=1552616768; Hm_lpvt_ce3365747bc6e46f69b1506dbb7b55ba=1552616768; Hm_lvt_f78f25b92eebf21f3f6fcb3e35be1516=1552616771; Hm_lpvt_f78f25b92eebf21f3f6fcb3e35be1516=1552616771; Hm_lvt_e81d7f51b76a84681a000c9162b4d13e=1552616771; Hm_lpvt_e81d7f51b76a84681a000c9162b4d13e=1552616771; Hm_lvt_08ef5961d6a494d8186b807e6509a52e=1552616771; Hm_lpvt_08ef5961d6a494d8186b807e6509a52e=1552616771; Hm_lvt_a1a86043f4a1a06bbaab7086fb8b8423=1552616771; Hm_lpvt_a1a86043f4a1a06bbaab7086fb8b8423=1552616771; CNZZDATA1257642703=241826669-1544753266-https%253A%252F%252Fwww.baidu.com%252F%7C1552613119; Hm_lvt_101f8389e3360b98e7ba58818fa7bdf8=1552616773; Hm_lpvt_101f8389e3360b98e7ba58818fa7bdf8=1552616773; CNZZDATA5890382=cnzz_eid%3D1066910384-1538048671-%26ntime%3D1552628022; iask_cookie=15526300069240.9786653745503371; CNZZDATA1254164143=127631358-1538050196-%7C1552630005; pt_s_3cc7b305=vt=1552630012378&cad=; pt_3cc7b305=uid=ZV/2FW7MZJinGTBvbhjrEw&nid=0&vid=/rCtxqzWK6BICmRw3hVJxA&vn=4&pvn=1&sact=1552630054961&to_flag=0&pl=G-84LZYETWqN8nQx7LCOxQ*pt*1552630012378; search_word1552630054973=%E7%94%B5%E8%84%91; search_word1552630082403=%E7%94%B5%E8%84%91; Hm_lpvt_ad29670c49e093f8aa6cbb0f672c1a81=1552630083',
        'Referer': 'https://iask.sina.com.cn/',
        # 'If-Modified-Since': 'Fri, 15 Mar 2019 06:08:00 GMT',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }
    url = 'https://iask.sina.com.cn/search?' + urlencode(params)
    print(url)

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except requests.ConnectionError:
        return None


#解析提取页面主要内容
def get_question(html):
    qt_data = []

    doc = pq(html)
    items = doc('.iask-search-main .iask-search-list > li').items()

    for item in items:
        xx = item.find('.num-text').items()#类型为生成器
        view_number = next(xx).text()
        answer_num = next(xx).text()
        question = {
            'qt_name':item.find('.title-text').text(),#问题详情
            'qt_url':'https://iask.sina.com.cn'+item.find('.title-text > a ').attr('href'),#问题链接
            'qt_detal':item.find('.list-text').text(),#答案
            'category':item.find('.label-text').text(),#问题分类
            'view_number':view_number,#浏览者人数
            'answer_num':answer_num#回答个数
        }
        print(question)
        qt_data.append(question)
    return qt_data

#将爬取的结果存入mongodb中
def save_to_mongo(question):
    try:
        collection.insert_one(question)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    print("开始抓取爱问知识人问题并保存至数据库")
    keywords = '电脑'
    all_datas = []
    for page in range(1,3):
        text = get_text(page,keywords)
        p_data = get_question(text)
        all_datas.extend(p_data)

    print("问题爬取结束，开始存储到Mongodb中...")
    # for q in all_datas:
    #     save_to_mongo(q)

    print("问题存储结束！")