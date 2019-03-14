#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/3/1 16:16
software: PyCharm
description: 猫眼电影Top100爬取
'''
import requests,re
import json,time
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?<a.*?>(.*?)</a>.*?star.*?>(.*?)</p>'
        '.*?releasetime.*?>(.*?)</p>.*?score.*?>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',re.S
    )
    results = re.findall(pattern,html)
    for result in results:
        yield {
            'index':result[0],
            'image':result[1],
            'title':result[2].strip(),
            'actor':result[3].strip()[3:] if len(result[3]) > 3 else '',
            'time':result[4].strip()[5:] if len(result[4]) > 5 else '',
            'score':result[5].strip()+result[6].strip()
        }

def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    # print(html)
    for item in parse_one_page(html):
        write_to_file(item)

def write_to_file(content):
    with open('rersult.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')

if __name__ == '__main__':
    scale = 100
    print("正在爬取猫眼Top100电影名单".center(scale // 2, "-"))  # .center() 控制输出的样式，宽度为 25//2，即 22，汉字居中，两侧填充 -
    for i in range(10):
        print("正在爬取猫眼Top100电影名单,第"+str(i+1)+"页...........")
        main(offset=i*10)
        time.sleep(1)

    print("爬取结束，已经保存到本地！")