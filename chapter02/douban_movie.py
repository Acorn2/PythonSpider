#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/1 18:32
software: PyCharm
description: 
'''
import requests,re
import time
import json
from requests.exceptions import RequestException

def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }
    try:
        res = requests.get(url,headers=headers)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile(
        '<li>.*?pic.*?class.*?>(.*?)</em>.*?img.*?src="(.*?)".*?title.*?>(.*?)</span>.*?bd.*?class.*?>(.*?)<br>(.*?)</p>.*?rating_num.*?>(.*?)</span>.*?<span>(.*?)</span>.*?quote.*?inq.*?>(.*?)</span>.*?</li>', re.S
    )
    # pattern = re.compile(
    #     '<li>.*?pic.*?class.*?>(.*?)</em>.*?</li>',
    #     re.S
    # )
    results = re.findall(pattern, html.replace('&nbsp;', ''))
    for result in results:
        if "主演" in result[3].strip():
            director = str(result[3].strip().split("主演:")[0][3:])
            actor = result[3].strip().split("主演:")[1]
        elif "主" in result[3].strip():
            director = result[3].strip().split("主")[0][3:]
            actor = ''
        else:
            director = result[3].strip()[3:]
            actor = ''

        if "/" in result[4].strip():
            time = result[4].strip().split("/")[0]+"/"+result[4].strip().split("/")[1]
            topic = result[4].strip().split("/")[2]
        else:
            time = result[4].strip()
            topic = " "

        yield {
            'index': result[0],
            'image': result[1],
            'title': result[2].strip(),
            'director':director,
            'actor': actor,
            'time':time,
            'topic':topic,
            'score':result[5],
        }

def main(offset=0):
    url = 'https://movie.douban.com/top250?start='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        # print(item)
        write_to_file(item)
    # print(html)

def write_to_file(content):
    with open('douban.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

if __name__ == '__main__':
    scale = 100
    print("正在爬取豆瓣Top100电影名单".center(scale // 2, "-"))  # .center() 控制输出的样式，宽度为 25//2，即 22，汉字居中，两侧填充 -
    for i in range(4):
        print("正在爬取豆瓣Top100电影名单,第" + str(i + 1) + "页...........")
        main(offset=i * 25)
        time.sleep(1)

    print("爬取结束，已经保存到本地！")